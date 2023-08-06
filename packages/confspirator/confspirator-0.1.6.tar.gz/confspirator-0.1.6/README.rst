CONFspirator: Plot better configs!
==================================

.. image:: http://img.shields.io/pypi/v/confspirator.svg
    :target: https://pypi.python.org/pypi/confspirator

An offshoot of OpenStack's Oslo.config with a focus on nested
configuration groups, and the ability to use yaml.

CONFspirator drops any command-line integrations, or file reading (for now)
and expects you to pass in a dictionary which will be parsed against the
defined groups. This lets the library for now focus on in-code defaults
and config field parsing.

What it can do
--------------

CONFspirator focuses on ConfigGroups and registering config fields onto them.
With groups themselves being able to be registered on parent groups.

It can also support lazy loading of config for dynamic groups where configs
must be registered dynamically from plugins or for other reasons.

Installation
------------

::

    pip install confspirator

Usage
-----

First lets put together a simple ConfigGroup, and register some config values::

    # ./root_conf.py
    from confspirator import groups, fields

    my_root_group = groups.ConfigGroup("my_app")
    my_root_group.register_child_config(
        fields.StrConfig("top_level_config", default="some_default"))

    sub_group = groups.ConfigGroup("sub_section")
    sub_group.register_child_config(fields.BoolConfig("bool_value"))
    my_root_group.register_child_config(sub_group)

Now we want to load in our config against this group definition and
check the values::

    import confspirator
    from root_conf import my_root_group

    conf_dict = {
        "my_app": {
            "top_level_config": "not_the_default",
            "sub_section": {
                "bool_value": True
            }
        }
    }
    CONF = confspirator.load(my_root_group, conf_dict)

    print(CONF.top_level_config)
    print(CONF.sub_section.bool_value)d

TODO
----

- reader logic for reading in data from yaml, json and ini files.
- exporting an example config
- potential command-line integrations
