TAG=$(uuidgen)
APP=$(basename $(pwd))
OUTDIR=/tmp/${APP}

rm -fr ${OUTDIR}
mkdir -p ${OUTDIR}

git tag ${TAG}

git archive --format tar --prefix ${APP}/ ${TAG} > ${OUTDIR}/rc.tar

cd ${OUTDIR}

tar xvf rc.tar

cd ${APP}
python -m mpremote fs rm -r :/apps/${APP}
python -m mpremote fs mkdir :/apps/${APP}
python -m mpremote fs cp -r * :/apps/${APP}
