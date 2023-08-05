#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Rick Hwang
# Mail: rick_kyhwang@hotmail.com
# Created Time: 2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
  name = "cops",
  version = "0.1.1",
  keywords = ("pip", "aws", "ec2", "provision", "infra", "iac", "rickhwang"),
  description = "Cloud operation utilities",
  long_description = "Cloud operation utilities for IAM, Policy, EC2 provisioning.",
  license = "MIT Licence",

  url = "https://github.com/rickhw/pipProject",
  author = "Rick Hwang",
  author_email = "rick_kyhwang@hotmail.com",

  packages = find_packages(),
  include_package_data = True,
  platforms = "any",
  install_requires = [],
  entry_points={
        'console_scripts': [
            'jujube=cops'
        ]
    }
)