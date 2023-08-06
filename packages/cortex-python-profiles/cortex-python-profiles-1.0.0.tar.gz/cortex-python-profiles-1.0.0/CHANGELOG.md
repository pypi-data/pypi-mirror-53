This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Upgrades from major to major versions, such a change from version `5.6.0` to `6.0.0`, might require local configuration updates to ensure compatibility with your current scripts. Make sure you have the latest version of the SDK using `pip install -U cortex-python-profiles`.


## [1.0.0] - 2019-09-20
### Added
* Seperated beta functionality of Po1 as a standalone package. 
* New Builders to Help Build Attributes and Push the appropriate events to creates Profiles.
  * This includes a ProfilesBuilder extension class to the cortex-python-builders package. 
  * This also includes attribute builders to help build attributes from feedback and insights.
* Synthesizors to help synthesize attributes, and the optional data they can be derived from
* ProfileClient extension to the cortex-python package to help access profiles and profile schemas
* ProfileSchema tempaltes to help users build profile schemas for profiles that this library can help derive attributes for.


