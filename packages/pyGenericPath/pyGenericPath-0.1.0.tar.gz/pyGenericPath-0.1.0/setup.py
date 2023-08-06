# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
#
# =============================================================================
#               ____                      _      ____       _   _
#  _ __  _   _ / ___| ___ _ __   ___ _ __(_) ___|  _ \ __ _| |_| |__
# | '_ \| | | | |  _ / _ \ '_ \ / _ \ '__| |/ __| |_) / _` | __| '_ \
# | |_) | |_| | |_| |  __/ | | |  __/ |  | | (__|  __/ (_| | |_| | | |
# | .__/ \__, |\____|\___|_| |_|\___|_|  |_|\___|_|   \__,_|\__|_| |_|
# |_|    |___/
#
# =============================================================================
# Authors:						Patrick Lehmann
#
# Python package:	    A generic path to derive domain specific path libraries.
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2017-2019 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
import setuptools

with open("README.md", "r") as file:
	long_description = file.read()

setuptools.setup(
	name="pyGenericPath",
	version="0.1.0",
	author="Patrick Lehmann",
	author_email="Paebbels@gmail.com",
	description="A generic path implementation to derive domain specific path libraries.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Paebbels/pyGenericPath",
	packages=setuptools.find_packages(),
	classifiers=[
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Development Status :: 2 - Pre-Alpha",
#		"Development Status :: 3 - Alpha",
#		"Development Status :: 4 - Beta",
#		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities"
	],
	python_requires='>=3.5',
)
