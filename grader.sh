#!/usr/bin/env bash

ASSIGNNAME="warntrash"
EXPERS="war trash"
METRICS="n l t"
GOLD_SEED=46347
GOLD_RUNS=25000
EXAMPLE_SEEDS="11473 483384 6363"
EXAMPLE_N=3
EXAMPLE_RUNS=800
GRADE_SEED=12345
GRADE_RUNS=1000
experiment()
{
	local theSIM="${1}"
	local game="${2}"
	local RUNS="${3}"
	local SEED="${4}"		
	local missingdata=0
	local residfmt="__residual-%s-%s-%d.%s"
	local residrand
	local residoutput

    echo -n >&2 $S $RUNS " "
    for ((i=0; i<${RUNS}; i++)); do 
        test $(( $i % 100 )) -eq 0 && echo -n >&2 $i " "
        residrand=`printf ${5:-${residfmt}} $S random $i dat 2>/dev/null`
        residoutput=`printf ${5:-${residfmt}} $S output $i log 2>/dev/null`
        "${theSIM}" ${game} \
                <(Random $(( SEED + i )) |tee "${residrand}" )  \
                | tee "${residoutput}" \
                | "${SIMGRADING}/output-pipe" | tr '\n' ' '  
        echo
    done | awk \
            -v dat1=__n-${S}-$SEED-$RUNS.dat \
            -v dat2=__t-${S}-$SEED-$RUNS.dat \
            -v dat3=__l-${S}-$SEED-$RUNS.dat \
            '{ print $1 >dat1; print $2 >dat2; print $3 >dat3; }'
	echo ${RUNS} >&2

	for m in ${METRICS} ; do 
	    test `ncdat "__${m}-${S}-${SEED}-${RUNS}.dat"` -ne ${RUNS} && missingdata=1   
	done

	for m in ${METRICS} ; do 
		for x in _${m}-${game}-${SEED}-${RUNS}.dat ; do
			lineswithdata "_${x}" | sort -g |${SIMGRADING}/ecdf >${x}
		done
	done


	return ${missingdata}
}

###
# SIMS and usage should be defined before sourcing sim-lib.sh
###
SIMS="war trash"
usage()
{
	cat <<EoT
ASSIGNMENT SPECIFIC OPTIONS 

  $ /assignment/specific/path/grader.sh . [RUNS [SEED]]

Where

  . is the SIM location (required first parameter)

  RUNS is the number of RUNS to use for SIM execution and plot generation

  SEED is a positive integer for a SEED to use for random file inputs

To retain residual data files to (maybe) assist in debugging, export

  $ export GRADER_SAVE_RESIDUALS=war

or 

  $ export GRADER_SAVE_RESIDUALS=trash

EoT
}

# if SIMGRADING is unknown
test -z "${SIMGRADING}" -a -r ~khellman/SIMGRADING/sim-lib.sh && ~khellman/SIMGRADING/setup.sh ~khellman/SIMGRADING
if ! test -r "${SIMGRADING}/sim-lib.sh" ; then
	cat >&2 <<EoT
ERROR:  SIMGRADING is not in your environment or SIMGRADING/sim-lib.sh cannot
be found.  Have you followed the grader tarball setup.sh instructions on the
assignment's Wiki page?
EoT
	exit 1
fi

test -n "${SIMGRADING}" && source "${SIMGRADING}/sim-lib.sh"

set -e

RUNS=${1:-${GRADE_RUNS}}
SEED=${2:-${GRADE_SEED}}


cat <<EoT |grader_msg 
Running SIM war and SIM trash with non-existent trace file.  These runs should
exit with non-zero status and without OUTPUT lines...
EoT
set +e   # disregard exit status
for S in ${SIMS} ; do 
	test_nonexist_tracefile "${simloc}/SIM" ${S} MISSINGRANDOM
done


grader_msg <<EoT
Running SIM war and SIM trash with truncated trace file.  These runs should
exit with non-zero status and without OUTPUT lines...
EoT
set +e   # disregard exit status
for S in ${SIMS} ; do 
	test_truncated_tracefile "${simloc}/SIM" ${S} TRUNCRANDOM
done


grader_msg <<EoT
Running many SIM experiments with varying seeds.  This may take 
some time ...
EoT
set -e
missingdata=0
for S in ${EXPERS} ; do
	experiment "${simloc}/SIM" ${S} ${RUNS} ${SEED}
	missingdata=$?

    grader_msg <<EoT
... generating comparison plots for ${S} ...
EoT
    for x in ${METRICS} ; do 
		gplotpdf ${x} ${S} ${RUNS} ${SEED}
    done

	grader_cleanup_experiment ${missingdata} "${METRICS}" "${S}" "${RUNS}" "${SEED}"

    grader_save_residuals ${S}

done

grader_signoff ${RUNS} ${SEED}
