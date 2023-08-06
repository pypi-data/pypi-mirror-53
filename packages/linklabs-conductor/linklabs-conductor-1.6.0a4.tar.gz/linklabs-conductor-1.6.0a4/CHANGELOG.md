# [1.6.0a4] - 2019-
### Added
- Unit Testing.
- Generated Documenation.
- Cypress and Nordic SLAP Message Specifications.
- Location Beacon Message Specifications.
- Alert Tag Message Specifications.
- Airfinder Base Class for Airfinder Objects.
- Node Base Class for SymBLE EndNodes.
- Extensible UplinkMessage Types for each Device.
- Added properties and data handling for different devices and base classes.
- UAT Instance to supported INSTANCES.
- Gateway Get Status (from new Status uplink).
- Generic Version Util.

### Changed
- Broke up library into submodules and individual files.

## Deprecated
- Conductor.INSTANCE, now passed through the construction of a Conductor Account
  or an Airfinder User.

# [1.6.0a3] - 2019-08-06
# Added
- Basic airfinder calls and stubs for future implementations.

# [1.6.0a2] - 2019-07-23
### Added
- HOSPITALITY to conductor INSTANCES.

### Changed
- Continued major library re-architecture.

# [1.6.0a1] - 2019-03-25
### Added
- conductor.INSTANCE to modify Instance, supports DEVELOP, CONDUCTOR
- LTEm Module and associated functions.
- Basic airfinder calls and stubs for future implementations.

### Changed
- Performed major library re-architecture.

## [1.5.4] - 2018-06-19
### Added
- Added methods for getting event counts from accounts and subjects (modules, gateways)

## [1.5.4b2] - 2018-06-11
### Fixed
- Fixed paging for retrieving larger volumes of messages

## [1.5.4b1] - 2018-05-07
### Added
- Support for additional node types
- Unpacking LTE-M specific module packet signal data
- Added method to get a subject's last seen time.
- Added method to get all nodes associated with an application token.
- Added support for Asset Groups (Create Groups, Delete Groups, Get Groups,
  Add Modules, Remove Modules, Get Modules, and Rename Groups)
### Fixed
- Remove dependence on sometime non-present fields in API uplink events
- Fixed HTTP calls in retrieving status messages

## [1.5.2] - 2017-2-1
### Fixed
- Set gateway's network token to None instead of throwing `KeyError` when
gateway has not been registered.

## [1.5.1] - 2017-1-4
### Added
- Added user-settable "on_close" callback for subscriptions.

### Changed
- Default UplinkMessage.network_token to None if it's not set in Conductor.

## [1.5.0] - 2016-10-28
### Changed
- Implement __eq__ and others for classes.
- Use Conductor's "next page" concept to split large queries into multiple
requests.

### Deprecated
- Deprecate get_messages_time_range_chunked, as chunking large queries
is now handled automatically.

## [1.4.0] - 2016-9-19
### Added
- Initial release. Includes functionality for querying data and metadata
for uplink messages from app tokens, network tokens, gateways, modules,
and accounts.
- Can send downlink messages to modules (unicast) and app tokens (multicast).
- Can query for status of downlink messages and cancel downlink messages.
- Can get data about subjects through the common _data attribute.
