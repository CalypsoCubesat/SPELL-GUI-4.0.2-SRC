################################################################################
#
#  Copyright (C) 2008, 2017 SES ENGINEERING, Luxembourg S.A.R.L.
#
#  This file is part of SPELL.
#
#  SPELL is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SPELL is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SPELL. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

#==============================================================================
# HELPER FUNCTIONS
#==============================================================================

function check_env_variable() {
    DST=${!1}
    if [ -z $DST ]; then
        echo "$1 is not set, defaulting to $2"
        export $1=$2
    fi
    DST=${!1}
    if [ ! -d $DST ]; then
        echo "ERROR: cannot find $1 directory: $DST"
        return 1
    else
        return 0
    fi
}

#==============================================================================
# ENVIRONMENT VARIABLES FOR SPELL-GUI
#==============================================================================

echo ">>> SPELL-GUI environment setup begin"

! check_env_variable SPELL_HOME /home/spell/SPELL && return 1
! check_env_variable SPELL_DATA $SPELL_HOME/data && return 1
! check_env_variable SPELL_CONFIG /home/spell/SPELL_CONFIG && return 1
! check_env_variable SPELL_LOG $SPELL_HOME/log && return 1

echo "*** SPELL_HOME=$SPELL_HOME"
echo "*** SPELL_DATA=$SPELL_DATA"
echo "*** SPELL_CONFIG=$SPELL_CONFIG"
echo "*** SPELL_LOG=$SPELL_LOG"

echo ">>> SPELL-GUI environment setup and validation done"
echo
