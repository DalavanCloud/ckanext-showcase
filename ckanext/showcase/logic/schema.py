import logging
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from ckan.lib.navl.validators import (not_empty,
                                      empty,
                                      unicode_safe,
                                      if_empty_same_as,
                                      ignore_missing,
                                      ignore,
                                      keep_extras)
from ckan.logic.validators import (package_id_not_changed,
                                   name_validator,
                                   user_id_or_name_exists,
                                   package_name_validator,
                                   tag_string_convert,
                                   ignore_not_package_admin,
                                   no_loops_in_hierarchy,
                                   no_http)
from ckan.logic.schema import (default_tags_schema,
                               default_extras_schema,
                               default_resource_schema)

from ckanext.showcase.logic.validators import (
    convert_package_name_or_id_to_id_for_type_dataset,
    convert_package_name_or_id_to_id_for_type_showcase,
    convert_group_names_to_group_objects)

log = logging.getLogger(__name__)


def showcase_base_schema():
    schema = {
        'id': [empty],
        'revision_id': [ignore],
        'name': [not_empty, unicode, name_validator, package_name_validator],
        'title': [if_empty_same_as("name"), unicode],
        'author': [ignore_missing, unicode],
        'author_email': [ignore_missing, unicode],
        'notes': [ignore_missing, unicode],
        'url': [ignore_missing, unicode],
        'state': [ignore_not_package_admin, ignore_missing],
        'type': [ignore_missing, unicode],
        'log_message': [ignore_missing, unicode, no_http],
        '__extras': [ignore],
        '__junk': [empty],
        'resources': default_resource_schema(),
        'tags': default_tags_schema(),
        'tag_string': [ignore_missing, tag_string_convert],
        'extras': default_extras_schema(),
        'save': [ignore],
        'return_to': [ignore],
        'groups': [ignore_missing, convert_group_names_to_group_objects],
    }

    # Extras
    schema['image_url'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['original_related_item_id'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['related_datasets'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['related_stories'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['story_date'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['story_type'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['methodology'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['spatial_text'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['author_title'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['author_workplace'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]
    schema['author_profile'] = [
        toolkit.get_validator('ignore_missing'),
        toolkit.get_converter('convert_to_extras')]

    # Extras (conditional)
    if config.get('disqus.name'):
        schema['allow_commenting'] = [
            toolkit.get_validator('ignore_missing'),
            toolkit.get_validator('boolean_validator'),
            toolkit.get_converter('convert_to_extras')]

    return schema


def showcase_create_schema():
    return showcase_base_schema()


def showcase_update_schema():
    schema = showcase_base_schema()

    # Users can (optionally) supply the package id when updating a package, but
    # only to identify the package to be updated, they cannot change the id.
    schema['id'] = [ignore_missing, package_id_not_changed]

    # Supplying the package name when updating a package is optional (you can
    # supply the id to identify the package instead).
    schema['name'] = [ignore_missing, name_validator,
                      package_name_validator, unicode]

    # Supplying the package title when updating a package is optional, if it's
    # not supplied the title will not be changed.
    schema['title'] = [ignore_missing, unicode]

    return schema


def showcase_show_schema():
    schema = showcase_base_schema()
    # Don't strip ids from package dicts when validating them.
    schema['id'] = []

    schema.update({
        'tags': {'__extras': [keep_extras]}})

    schema.update({
        'state': [ignore_missing],
        })

    schema['groups'] = {
        'name': [not_empty, no_loops_in_hierarchy, unicode_safe],
        'capacity': [ignore_missing],
        '__extras': [ignore],
        'description': [ignore_missing],
        'display_name': [ignore_missing],
        'image_display_url': [ignore_missing],
    }

    # Remove validators for several keys from the schema so validation doesn't
    # strip the keys from the package dicts if the values are 'missing' (i.e.
    # None).
    schema['author'] = []
    schema['author_email'] = []
    schema['notes'] = []
    schema['url'] = []

    # Add several keys that are missing from default_create_package_schema(),
    # so validation doesn't strip the keys from the package dicts.
    schema['metadata_created'] = []
    schema['metadata_modified'] = []
    schema['creator_user_id'] = []
    schema['num_tags'] = []
    schema['revision_id'] = []
    schema['tracking_summary'] = []

    # Extras
    schema['image_url'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['original_related_item_id'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['related_datasets'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['related_stories'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['story_date'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['story_type'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['methodology'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['spatial_text'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['author_title'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['author_workplace'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]
    schema['author_profile'] = [
        toolkit.get_converter('convert_from_extras'),
        toolkit.get_validator('ignore_missing')]

    # Extras (conditional)
    if config.get('disqus.name'):
        schema['allow_commenting'] = [
            toolkit.get_converter('convert_from_extras'),
            toolkit.get_validator('boolean_validator'),
            toolkit.get_validator('ignore_missing')]

    return schema


def showcase_package_association_create_schema():
    schema = {
        'package_id': [not_empty, unicode,
                       convert_package_name_or_id_to_id_for_type_dataset],
        'showcase_id': [not_empty, unicode,
                        convert_package_name_or_id_to_id_for_type_showcase]
    }
    return schema


def showcase_package_association_delete_schema():
    return showcase_package_association_create_schema()


def showcase_package_list_schema():
    schema = {
        'showcase_id': [not_empty, unicode,
                        convert_package_name_or_id_to_id_for_type_showcase]
    }
    return schema


def package_showcase_list_schema():
    schema = {
        'package_id': [not_empty, unicode,
                       convert_package_name_or_id_to_id_for_type_dataset]
    }
    return schema


def showcase_admin_add_schema():
    schema = {
        'username': [not_empty, user_id_or_name_exists, unicode],
    }
    return schema


def showcase_admin_remove_schema():
    return showcase_admin_add_schema()
