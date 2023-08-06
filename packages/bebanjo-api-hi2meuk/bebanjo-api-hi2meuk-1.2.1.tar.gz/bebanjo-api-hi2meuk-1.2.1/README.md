# Bebanjo API client

A client library interfacing to Bebanjo's Movida and Sequence APIs allowing integration developers to focus on the business logic of their application and not the low level detail.

The library provides support for authentication, exception handling, logging and utilities for common tasks. It can be used in an interactive session. By design it is very loosely coupled to Movida/Sequence schemas.

## Example Application

To demonstrate some features, here is an application to upload an image on all titles scheduled on platform `Android GB` and target them for that platform and set them as the `post art` for that title in the Movida UI.


``` python
from bebanjo import MovidaAPI

mapi = MovidaAPI(env='staging')

IMAGE_URL = 'tests/image/1yeVJox3rjo2jBKrrihIMj7uoS9.JPEG'

platforms = mapi.platforms.fetch()
target_platform = filter(lambda p: p.name == 'Android GB', platforms)[0]
for title in target_platform.titles.get_paginated():
    image = title.images.create_image(IMAGE_URL, meta1={'IsPosterArt': True})
    image.target_platforms.create(target_platform.url)
```

> Although this would work as described, a well designed application would also include exception handling, checking if the image already exists and logging to file.

## Installation

### PyPI

``` bash
pip install --user bebanjo-api
```

### GIT

Visit [bebanjo-api](https://gitlab.com/hi2meuk/bebanjo-api) in **GitLab** to clone and contribute to the project.

## Using the Bebanjo client library

### Setting up your application

``` python
from bebanjo import MovidaAPI, install_auth_handlers
```

#### Robot account credentials

The authentication handler must be initialised with login data for the Bebanjo environments used.  The library assumes there no distinction between Sequence and Movida credentials. The format of the credentials to be supplied to the handler initialisation is a nested dict as follows:

``` python
config = {
    'staging': {
        'name': 'robot_hi2meuk',
        'password': 'mypassword'
    }
}
```

> The environment key(s) must be one of: `staging`, `preproduction` or `production`.

Setup the authentication handler before instantiating an API providing a config data structure as previously described:

``` python
install_auth_handlers(config)
```

A function is provided by the library to setup the auth config based on a local JSON file.

``` python
from bebanjo.utils import read_local_config
config = read_local_config(CONFIG_FILE)
```

> The config file must be in JSON format. If a file path is not supplied, the default is ".bebanjo.json" in users home directory (Windows or Linux).

#### Create a Movida API instance for your chosen environment

``` python
mapi = MovidaAPI(env='staging')
```

It is possible to specify a local Wiremock server to emulate Movida/Sequence for component testing purposes:

``` python
mock_url = 'http://localhost:8080/api'
mapi = MovidaAPI(url=mock_url)
```

#### Logging

API calls made and responses are logged using the [python logging framework](https://docs.python.org/3.7/howto/logging.html#logging-advanced-tutorial).

Logs are generated at debug level containing the XML payloads sent and received.  Console output only includes logs of severity WARNINGS and above. This is a characteristic of the logging framework.  The following code placed in the application will enable DEBUG to the console with in the format specified.

``` python
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
```

## Principals of use

### Fetch first to discover what the next thing does

Imagine you are to navigate the Movida API and your **only** knowledge and starting point is the root: `/api`. You would first have to do a GET call that resource to find it contains other collection resources (REST collection) like `titles` and `title_groups` and others.  If you made a GET call on the `titles` resource you will notice it has numerous metadata keys and values and `links` to other collection resources including extended `Metadata`. Likewise, you would have to do a GET call on those resources e.g. `assets` to know what sort of resources it has.

The same applies to using this client library, often we have to do a fetch to access the properties beyond the API root.

This approach means the library is loosely coupled to Movida. If there are changes in Movida schema it is unlikely to require an update to this library.  it also means you do not have to tell the library about your companies custom metadata; the library will discover it and make it available to your application.

#### Except, no need to fetch root/api resource

There are exceptions to this "fetch first" principal. Because fetching the API is a common starting point and what it contains is very predictable, the library pre-populates the properties of the root API object, e.g. it already has a `titles` property:

``` python
mapi = MovidaAPI(env='staging')
title = mapi.fetch(1001)
```

#### Except, don't need to fetch the schedulings resource - use add_link() instead

If you want to avoid unnecessary GET calls when you know the next item beyond the current URL path, you can patch it in to your object.  A common use case is the schedule resource; when you fetch it, you find it only contains a link to the schedulings resource and nothing else.  We can add the schedulings resource directly and save a GET call.

``` python
mapi = MovidaAPI(env='staging')
title = titles.fetch(1001)
schedulings = title.schedule.add_link('schedulings').fetch()
```

## Features

### Memory efficient Collection processing

The get_paginated() method of a collection resource e.g. titles is a python generator.  It will iterate through each title of the resource returning each title at a time.  It will make the GET calls to Movida one page at a time as and when needed (by default with a page size of 50). Only the page of items is held in memory within the collection object at any time.

``` python
platform = mapi.platforms.fetch(101)
titles = platform.titles.get_paginated()
for title in titles:
    print(title.name)
```

### Image creation and setting the target platforms

Images can be uploaded from a local file or from a remote server location, the method will be determined from the file path given to the `create_image()` method.  The return value is an image object representing the created image.  Images can be created from a pre-fetched or post fetched object.  The encoding type and file name are by default extracted from the given image file name but can be overridden by passing in a dict object.  Other metadata can also be passed in.  Movida will set values for size and MD5 checksum when the file is processed - this is done asynchronously for remotely sourced images and will be empty in the locally created object.

``` python
IMAGE_PATH_LOCAL = 'tests/image/1yeVJox3rjo2jBKrrihIMj7uoS9.JPEG'
mapi = MovidaAPI(env='staging')
title = titles.fetch(1001)
image = title.images.create_image(IMAGE_PATH_REMOTE)
image.target_platforms.add_platforms(['https://movida.bebanjo.net/api/platforms/51', 'api/platforms/52', 53])
```

A remote path is also supported.

``` python
IMAGE_PATH_REMOTE = 'https://mydomain.com/image/1yeVJox3rjo2jBKrrihIMj7uoS9.jpg'
```

For existing images there is a risk the addition of a target_platform will fail if it already exists on the image.

``` python
images = title.images.fetch()
for image in images:
    if image.type == SELECTED_IMAGE_TYPE:
    image = image.fetch()
    image.target_platforms.add_platforms(TARGET_PLATFORMS)  # will fail if any exists already
```

To avoid the possible failure do:

``` python
    image = image.fetch()
    image.target_platforms = image.target_platforms.fetch()  # get existing target platforms
    image.target_platforms.add_platforms(TARGET_PLATFORMS)   # will not add platform if already exists
```

Note the long code line in the above:

``` python
image.target_platforms = image.target_platforms.fetch()
```

This is necessary when target_platforms is of class Fetcher; it cannot *upgrade* its own class to Collection.  A helper is available to make the code a little cleaner.

``` python
from bebanjo.utils import replace_self_fetch

replace_self_fetch(image.target_platforms)
```


### Seamlessly step between Movida and Sequence

As long as you have valid credentials loaded that are valid for Movida and Sequence, then the library does is agnostic to the resource referenced in an object property. E.g. the jobs resource on a Movida scheduling refers to a resource in Sequence and accessing that resource will automatically trigger authentication with Sequence.

### String representations of an object

#### Inspect utility

Inspect the properties of a title; first class metadata, extended metadata and links to related objects that can be fetched for further inspection.  It prints directly to the console.  It is intended for debugging and interactive sessions.

``` python
from bebanjo import inspect
inspect(title)
```

Output:

```
Instance of Title (//titles/1001)
 > name: Winter Is Coming
 > title: Winter Is Coming
 > external_id: 63056
 > title_type: 'episode
 > episode_number: 1
 > tags:
 Metadata:
 > short_description: The "one" where winter's comming
 > air_date: 2011-04-24
 > content_source: The Movie Database
 > subgenres: ['Action', 'Fantasy']
 > download_rights: True
 Getters:
 > assets
 > availability_windows
 > blackouts
 > images
 > licensor
 > linear_schedulings
 > metadata
 > rights
 > rules
 > schedule
 > title_groups
 > trailers
 ```

#### Fetch a title by external ID

``` python
title = mapi.titles.fetch(1001)
```

### Fetch title by external_id and include extended metadata and images

``` python
title = mapi.titles.fetch(external_id='HI2MEUK/377364', expand=['metadata', 'images'])
```

### Fetch asset by name

``` python
asset = mapi.assets.fetch(name='BBJ12345A')
```

### Create an object using the parent resource object

No need to fetch the collection resource first as only it's URL is needed to create an object inside this resource.

``` python
mapi = MovidaAPI(env='staging')
meta = {'name': 'The Ring'}
relations = {'licensor': 'api/licensors/4'}
mapi.titles.create(meta, relations)
```

> In the above example, if name were not specified, Movida would complain with a 422 response because `name` is mandatory for a title.  Likewise if a metadata key or value is invalid, a 422 response would also result.

### Read the metadata of an object

Access the values of metadata like they're python dictionary.

``` python
# first class metadata
name = title['name']
# extended metadata
description = title.metadata['description']
```

### Update a title in Movida

``` python
# first class metadata
title.update({'name': 'The Ring'}, {'licensor': 'api/licensors/1201'})
# extended metadata requires a seperate call to Movida
title.metadata.update({'name': 'abcdéf', 'description': 'Simon looses the ring.'})
```

### Build a dict of platform names to IDs

``` python
id_from_platform = {}
for platform in mapi.platforms.fetch():
    id_from_platform[platform.name] = platform.id
```
