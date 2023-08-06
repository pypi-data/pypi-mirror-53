import itertools
from sqlalchemy.sql.expression import any_
import time

from .grid import create_grid
from .impact import get_event_impact, make_inspection_priority
from .orm import (
    dbconnect,
    Event,
    Facility,
    FacilityShaking,
    Group,
    LocalProductType,
    LocalProduct,
    Notification,
    ShakeMap
)
from .products.geojson import generate_impact_geojson
from .util import Clock, SC, DAY
from .notifications.notifications import new_event_notification, inspection_notification


def can_process_event(event, scenario=False):
    # check if we should wait until daytime to process
    clock = Clock()
    sc = SC()
    if (clock.nighttime() is True) and (scenario is False):
        if event.magnitude < sc.night_eq_mag_cutoff:
            return False

    if ((sc.dict['Notification'].get('require_shakemap', False) is True)
            and (scenario is False)):
        if len(event.shakemaps) == 0:
            return False

    return True


@dbconnect
def check_new(session=None):
    '''
    Search database for unprocessed shakemaps

    Returns:
        dict: a dictionary that contains information about the function run
        ::
            data = {'status': either 'finished' or 'failed',
                    'message': message to be returned to the UI,
                    'log': message to be added to ShakeCast log
                           and should contain info on error}
    '''
    log_message = ''
    error = ''
    try:
        new_events = (session.query(Event)
                             .filter(Event.status == 'new')
                             .all())
        new_shakemaps = (session.query(ShakeMap)
                                .filter(ShakeMap.status == 'new')
                                .all())

        if new_events:
            process_events(new_events, session=session)
            log_message += '\nProcessed Events: %s' % [str(ne)
                                                       for ne in new_events]
        if new_shakemaps:
            process_shakemaps(new_shakemaps, session=session)
            log_message += '\nProcessed ShakeMaps: %s' % [
                str(sm) for sm in new_shakemaps]
        else:
            log_message += '\nNo new shakemaps'

    except Exception as e:
        error = '{}: {}'.format(type(e), str(e))
        log_message += 'failed to process new events/shakemaps: {}'.format(e)

    data = {'status': 'finished',
            'message': 'Check for new earthquakes',
            'log': log_message,
            'error': error}

    return data


def create_new_event_notifications(groups, event, scenario=False):
    notifications = []
    for group in groups:
        # check new_event magnitude to make sure the group wants a
        # notificaiton

        if event.type != 'heartbeat':
            event_spec = group.get_new_event_spec(scenario=scenario)
            if (event_spec is None or
                    event_spec.minimum_magnitude > event.magnitude):
                continue

        notification = Notification(group=group,
                                    event=event,
                                    notification_type='NEW_EVENT',
                                    status='created')

        notifications += [notification]

    return notifications


def create_inspection_notifications(groups, shakemap, scenario=False):
    notifications = []
    for group in groups:
        notification = Notification(group=group,
                                    shakemap=shakemap,
                                    event=shakemap.event,
                                    notification_type='DAMAGE',
                                    status='created')
        notifications += [notification]

    return notifications


@dbconnect
def get_inspection_groups(grid, scenario=False, session=None):
    if scenario is True:
        in_region = (session.query(Group)
                     .filter(Group.in_grid(grid))
                     .all())
        groups_affected = [group for group in in_region
                           if group.gets_notification('damage', scenario=True)]
    else:
        in_region = (session.query(Group)
                     .filter(Group.in_grid(grid))
                     .all())
        groups_affected = [group for group in in_region
                           if group.gets_notification('damage')]

    return groups_affected


@dbconnect
def get_new_event_groups(event, scenario=False, session=None):
    groups_affected = []
    all_groups_affected = set()
    if scenario is True:
        in_region = (session.query(Group)
                     .filter(Group.point_inside(event))
                     .all())
        groups_affected = [group for group in in_region
                           if group.gets_notification('new_event', scenario=True)]

        all_groups_affected.update(groups_affected)
    elif event.type.lower() != 'heartbeat':
        groups_affected = (session.query(Group)
                           .filter(Group.point_inside(event))
                           .all())

        filtered_groups = [group for group in groups_affected
                           if group.gets_notification('new_event')]

        all_groups_affected.update(filtered_groups)
    else:
        all_groups = session.query(Group).all()

        groups_affected = [group for group in all_groups
                           if group.gets_notification('new_event', heartbeat=True)]

        all_groups_affected.update(groups_affected)

    return all_groups_affected


@dbconnect
def get_new_event_notifications(group, scenario=False, session=None):
    '''
    Get notifications generated for this group from the last day
    '''
    # get new notifications
    notifications = (session.query(Notification)
                     .filter(Notification.notification_type == 'NEW_EVENT')
                     .filter(Notification.status == 'created')
                     .filter(Notification.group_id == group.shakecast_id)
                     .all())

    last_day = time.time() - 60 * 60 * 5
    filter_nots = filter(
        lambda x: x.event is not None and
        (x.event.time > last_day or scenario is True), notifications)

    return filter_nots


@dbconnect
def process_events(events=None, session=None, scenario=False):
    '''
    Process or reprocess events passed into the function. Will send
    NEW_EVENT and UPDATE emails

    Args:
        new_events (list): List of Event objects to process
        session (Session()): SQLAlchemy session

    Returns:
        dict: a dictionary that contains information about the function run
        ::
            data = {'status': either 'finished' or 'failed',
                    'message': message to be returned to the UI,
                    'log': message to be added to ShakeCast log
                           and should contain info on error}
    '''
    if events:
        all_groups_affected = set([])
        for event in events:
            if can_process_event(event, scenario) is False:
                if time.time() - DAY > event.time:
                    # timeout this event, it's been over a day
                    event.status = 'Not processed - Timeout'
                continue

            event.status = 'processing_started'
            groups_affected = get_new_event_groups(event, scenario, session)

            # if there aren't any groups, just skip to the next event
            if not groups_affected:
                event.status = 'processed - no groups'
                session.commit()
                continue

            new_notifications = create_new_event_notifications(
                groups_affected,
                event,
                scenario)
            session.add_all(new_notifications)
            session.commit()

            all_groups_affected.update(groups_affected)

        processed_events = []
        for group in all_groups_affected:
            notifications = get_new_event_notifications(group, scenario, session)
            if len(notifications) > 0:
                new_event_notification(notifications=notifications,
                                    scenario=scenario)

                processed_events += [n.event for n in notifications]

        for e in processed_events:
            e.status = 'processed' if scenario is False else 'scenario'

        return processed_events
    return []


def compute_event_impact(facilities, shakemap, grid):
    facility_shaking = [None] * len(facilities)
    count = 0
    for facility in facilities:
        fac_shaking = make_inspection_priority(facility=facility,
                                               shakemap=shakemap,
                                               grid=grid)
        if fac_shaking is False:
            continue

        facility_shaking[count] = FacilityShaking(**fac_shaking)
        count += 1

    return facility_shaking


@dbconnect
def process_shakemaps(shakemaps=None, session=None, scenario=False):
    '''
    Process or reprocess the shakemaps passed into the function

    Args:
        shakemaps (list): List of ShakeMap objects to process
        session (Session()): SQLAlchemy session
        scenario (boolean): True for manually triggered events

    Returns:
        dict: a dictionary that contains information about the function run
        ::
            data = {'status': either 'finished' or 'failed',
                    'message': message to be returned to the UI,
                    'log': message to be added to ShakeCast log
                           and should contain info on error}
    '''
    for shakemap in shakemaps:
        if can_process_event(shakemap.event, scenario) is False:
            continue
        shakemap.mark_processing_start()

        # open the grid.xml file and find groups affected by event
        grid = create_grid(shakemap)
        groups_affected = get_inspection_groups(grid, scenario, session)

        if not groups_affected:
            shakemap.mark_processing_finished()
            session.commit()
            continue

        # send out new events and create inspection notifications
        new_notifications = create_inspection_notifications(
            groups_affected, shakemap, scenario)

        session.add_all(new_notifications)
        session.commit()

        # get a set of all affected facilities
        affected_facilities = (session.query(Facility)
                               .filter(Facility.in_grid(grid))
                               .all())

        if affected_facilities:
            facility_shaking = compute_event_impact(
                affected_facilities, shakemap, grid)

            # Remove all old shaking and add all fac_shaking_lst
            shakemap.facility_shaking = []
            session.commit()

            session.bulk_save_objects(facility_shaking)
            session.commit()
        else:
            shakemap.mark_processing_finished()
            shakemap.status = 'processed - no facs'

            session.commit()
            continue

        # grab new notifications, and any that might have failed to send
        notifications = (session.query(Notification)
                         .filter(Notification.shakemap == shakemap)
                         .filter(Notification.notification_type == 'DAMAGE')
                         .filter(Notification.status == 'created')
                         .all())

        if notifications:
            # send inspection notifications for the shaking levels we
            # just computed
            for n in notifications:
                # generate pdf for specific group
                generate_local_products(n.group, n.shakemap, session=session)

                inspection_notification(notification=n,
                                        scenario=scenario,
                                        session=session)

        shakemap.mark_processing_finished()
        if scenario is True:
            shakemap.status = 'scenario'
        session.commit()

        # generate system level products
        generate_impact_geojson(shakemap, save=True)

    return shakemaps


@dbconnect
def generate_local_products(group, shakemap, session=None):
    if group.product_string is not None:
        local_product_names = group.product_string.split(',')
        product_types = session.query(LocalProductType).filter(
            LocalProductType.name.in_(local_product_names)).all()

        for product_type in product_types:
            # check if product exists
            product = (session.query(LocalProduct)
                    .filter(LocalProduct.group == group)
                    .filter(LocalProduct.shakemap == shakemap)
                    .filter(LocalProduct.product_type == product_type).first())

            if not product:
                product = LocalProduct(
                    group=group,
                    shakemap=shakemap,
                    product_type=product_type
                )

                product.name = (product_type.file_name or
                        '{}_impact.{}'.format(group.name, product_type.type))

            try:
                if (product.finish_timestamp and
                        product.finish_timestamp > product.shakemap.begin_timestamp):
                    continue

                product.generate()
                product.error = None
            except Exception as e:
                product.error = str(e)

            product.finish_timestamp = time.time()
            session.add(product)
        session.commit()


@dbconnect
def run_scenario(shakemap_id=None, session=None):
    '''
    Processes a shakemap as if it were new
    '''
    error = None

    # Check if we have the eq in db
    event = session.query(Event).filter(Event.event_id == shakemap_id).first()
    shakemap = session.query(ShakeMap).filter(
        ShakeMap.shakemap_id == shakemap_id).first()
    try:
        if event:
            process_events(events=[event],
                           session=session,
                           scenario=True)

        if shakemap:
            process_shakemaps(shakemaps=[shakemap],
                              session=session,
                              scenario=True)

        message = 'Scenario run complete'

    except Exception as e:
        error = str(e)
        message = 'Scenario run failed: {}'.format(error)

    if event is None and shakemap is None:
        error = 'No events available for this event id'

    return {'status': 'finished',
            'message': {'from': 'scenario_run',
                        'title': 'Scenario: {}'.format(shakemap_id),
                        'message': message,
                        'success': error is None},
            'error': error,
            'log': 'Run scenario: ' + shakemap_id}
