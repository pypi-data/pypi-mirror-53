#!/usr/bin/env bash
# vim: set fileencoding=utf-8 :

# connord - connect to nordvpn servers
# Copyright (C) 2019  Mael Stor <maelstor@posteo.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Ensure running script in openvpn environment
# shellcheck disable=2154
[[ "$script_type" ]] || exit 1

this_dir="$(dirname "$0")"
resolvconf='/sbin/resolvconf'
[[ -x "$resolvconf" ]] || exit 1

case "$script_type" in
  up)
    for optname in ${!foreign_option_*}; do
      [ -n "${optname}" ] || break

      read -ra opts <<< "${!optname}"
      opt=${opts[0]}
      _type=${opts[1]}
      remote=${opts[2]}

      [[ "${opt}" == "dhcp-option" ]] || continue
      if [[ "${_type}" == "DOMAIN" ]] || [[ "${_type}" == "DOMAIN-SEARCH" ]]; then
        result="search ${remote}\n${result}"
      elif [ "${_type}" = "DNS" ]; then
        result+="nameserver ${remote}\n"
      fi
    done
    echo -ne "$result" | "$resolvconf" -a "${dev}.openvpn"

    # shellcheck disable=1090
    source "${this_dir}/dump_openvpn_env.bash"
    ;;
  down)
    "$resolvconf" -d "${dev}.openvpn"

    # shellcheck disable=1090
    source "${this_dir}/dump_openvpn_env.bash"
    ;;
esac
