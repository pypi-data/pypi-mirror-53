======================
Django Digital Diocese
======================

Release Notes
=============

2.2.1
-----

- Fix thumbnail image for documents list
  https://github.com/developersociety/django-digitaldiocese/pull/255

- Replace Google Maps API key
  https://github.com/developersociety/django-digitaldiocese/pull/253

- Update the fake contact details in the footer
  https://github.com/developersociety/django-digitaldiocese/pull/252

2.2.0
-----

- Fix Latest Vacancies block images href to redirect to vacancy post

2.1.9
-----

- The DDC carousel
  https://github.com/developersociety/django-digitaldiocese/pull/237/

- For all sites, add to ``INSTALLED_APPS`` in `base.py`:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'digitaldiocese.carousel',
    ]

- Update base.html with new lightbox container and carousel javascript:
  https://github.com/developersociety/django-digitaldiocese/pull/237/files#diff-d537bc1af808aa8017003121118ea34c


2.1.8
-----

- Revert unpublished pages showing in navigation - use "Show in navigation" tickbox instead
  https://github.com/developersociety/django-digitaldiocese/pull/235


2.1.7
-----

- Unpublished pages showing in navigation
  https://github.com/developersociety/django-digitaldiocese/pull/232
  https://github.com/developersociety/django-digitaldiocese/pull/233

- More columns for the home page layout
  https://github.com/developersociety/django-digitaldiocese/pull/231


2.1.6
-----

- Fix vacancies queryset filter to display from and until
  https://github.com/developersociety/django-digitaldiocese/pull/228


2.1.5
-----

- Fix date display for news posts:
  https://github.com/developersociety/django-digitaldiocese/pull/226

- Add view protected page to groot group permissions:
  https://github.com/developersociety/django-digitaldiocese/pull/225

- Change test database name to avoid test collisions:
  https://github.com/developersociety/django-digitaldiocese/pull/223

- Bump fields up to higher max_length values to avoid ACNY (+ others) sync problems:
  https://github.com/developersociety/django-digitaldiocese/pull/221


2.1.4
-----

Fixes vacancies manager so use of model's 'display from' / 'display until' dates are correct:
https://github.com/developersociety/django-digitaldiocese/pull/220


2.1.3
-----

Fixes carousel link behavior in all default columns:
https://github.com/developersociety/django-digitaldiocese/pull/215/files


2.1.2
-----

Remove stray '{' character in Twitter share URL:
https://github.com/developersociety/django-digitaldiocese/pull/213


2.1.1
-----

Restricted Groot permission choices for Page admin (requires django-groot 0.1.1):
https://github.com/developersociety/django-digitaldiocese/pull/211


2.1.0
-----

Moved ACNY management commands into separate repo:
https://github.com/developersociety/django-digitaldiocese-achurchnearyou


2.0.1
-----

- Added the `geocode_churches` management command to update the geo location of Churches with a
  postcode, but no location: https://github.com/developersociety/django-digitaldiocese/issues/204

- Removed JavaScript error when viewing a Church without any location details:
  https://github.com/developersociety/django-digitaldiocese/issues/202


2.0.0
-----

Move towards separating out the various components of Digital Diocese.

Removed `worthers` app. Use https://github.com/developersociety/django-digitaldiocese-cofecms instead.


1.5.9
-----

- Reworked ACNY 'Regular Services' and 'Other Events' tabs.


1.5.8
-----

- Synchronizing events also pulls in date of recurring events.


1.5.7
-----

- ACNY search results are optional.

- Fix gaps in navigation under mobile view.

- Add location support for glitter-events 0.1.3 .

- Reduce the amount of events shown to 3 or 2, depending on context.


1.5.6
-----

- Carousel slide titles now link to pages in tablet/mobile view

- ACNY pages now have page titles that are relevant to their content.

- Postcode search block label corrected from 'q'.


1.5.5
-----

- News and Events can now optionally filteron tags

- In-page navigation is hidden in mobile view.

1.5.4
-----

- Worthers import now ensures imported URLs include the protocol.
  https://github.com/developersociety/django-digitaldiocese/issues/137

- Create separate includes for person details and detail footer on Church detail page.
  https://github.com/developersociety/django-digitaldiocese/issues/138,
  https://github.com/developersociety/django-digitaldiocese/issues/141

1.5.3
-----

- Close DD tag in acny church meta data.
  https://github.com/developersociety/django-digitaldiocese/issues/132

- Ensures missing ACNY church description doesn't create p tag.
  https://github.com/developersociety/django-digitaldiocese/issues/132


1.5.2
-----

- Ensures privacy settings in Worthers are being adhered to.
  https://github.com/developersociety/django-digitaldiocese/issues/90

- Support for Worthers `informal_name` field during data import.
  https://github.com/developersociety/django-digitaldiocese/issues/91

- Church model's `__str__` method no longer references its Parish. Large speed improvement when
  using Church/School blocks.
  https://github.com/developersociety/django-digitaldiocese/issues/88

- Added `WORTHERS_STRIP_STIPENDIARY = True` option, which will remove stipendiary suffices from
  role names.
  https://github.com/developersociety/django-digitaldiocese/issues/94

- Will now delete existing roles imported via the Worthers API, which no longer match
  `WORTHERS_ROLE_NAME_WHITELIST`.
  https://github.com/developersociety/django-digitaldiocese/issues/95

- Bug fix where Worthers contact import would error out on empty Contact Titles.
  https://github.com/developersociety/django-digitaldiocese/issues/110

- No longer show "None" items when listing places associated with a Person.
  https://github.com/developersociety/django-digitaldiocese/issues/108

- Some general fixes to show "School" instead of "Church" in the right context.
  https://github.com/developersociety/django-digitaldiocese/issues/98,
  https://github.com/developersociety/django-digitaldiocese/issues/100

- Abstracted parts of the Church detail page into separate includes.
  https://github.com/developersociety/django-digitaldiocese/issues/111,
  https://github.com/developersociety/django-digitaldiocese/issues/119

- Fixed subject line in Email share link.
  https://github.com/developersociety/django-digitaldiocese/issues/115

- Added `sort_by_role_name` template tag to sort a list of roles by role name.
  https://github.com/developersociety/django-digitaldiocese/issues/96

- Ensured Worthers Place update script brings in website addresses. Also added `--force` flag to
  ignore `updated_at` dates and update all places regardless.
  https://github.com/developersociety/django-digitaldiocese/issues/123


1.5.1
-----

- Small front-end tweaks
  https://github.com/developersociety/django-digitaldiocese/pull/89


1.5
---

- Integration support for Worthers.

- Single search feature allowing postcode and name searches to be performed from same search
  box. https://github.com/developersociety/django-digitaldiocese/issues/61

- `fixblocks` management command to remove misconfigured content blocks.
  https://github.com/developersociety/django-digitaldiocese/issues/73

- Generic search block, allowing a handy search block to be added to any page.
  https://github.com/developersociety/django-digitaldiocese/issues/77


1.4.2
-----

- Allow Vacancies to (optionally) only be shown between certain dates.
  https://github.com/developersociety/django-digitaldiocese/issues/55

- Responsive fix for ACNY columns
  https://github.com/developersociety/django-digitaldiocese/issues/57


1.4.1
-----

- Fix issue where most recently updated instance of a Person was not being selected during the
  `myd_update_people` process. https://github.com/developersociety/django-digitaldiocese/issues/51


1.4
---

- HTML tidying

- Fix pin popups for ACNY Google Maps


1.3
---

- Better links on Vacancies pages

- Use HTTPS for OpenLayers.js

- Increased size of Church `built` field from 50 to 150 chars

- More event attributes and labels handled

- Hide empty detail tabs on Church pages


1.2
---

- MyDiocese fixes.

- Multiple church block fixes.

- For sites with a custom `base.html`, add this before ``</body>``:

.. code-block:: htmldjango

    <script src="{% static 'acny/js/acny-map.js' %}"></script>

- Enable People specific functionality (e.g. if MyDiocese integration is active) with this
  setting in ``base.py``:

.. code-block:: python

    ENABLE_PEOPLE = os.environ.get('ENABLE_PEOPLE') == "1"


1.1
---

- MyDiocese integration.

- For all sites, add to ``INSTALLED_APPS`` in `base.py`:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'django.contrib.gis',
        'digitaldiocese.datawrangler',
    ]

- For sites using MyDiocese, add these settings to `base.py`:

.. code-block:: python

    MYD_DB_HOST = os.environ.get('MYD_DB_HOST')
    try:
        MYD_DB_PORT = int(os.environ.get('MYD_DB_PORT'))
    except TypeError:
        MYD_DB_PORT = 3306
    MYD_DB_USERNAME = os.environ.get('MYD_DB_USERNAME')
    MYD_DB_PASSWORD = os.environ.get('MYD_DB_PASSWORD')
    MYD_DB_DATABASE = os.environ.get('MYD_DB_DATABASE')

- For sites using MyDiocese, add ``myd_update`` to `fabfile.py`:

.. code-block:: text

    {myd}           /usr/local/bin/django-cron python manage.py myd_update

- For sites using MyDiocese, add these requirements to `requirements/base.txt`:

.. code-block:: text

    # MyDiocese
    mysqlclient==1.3.7


1.0
---

- Initial release for sites.
