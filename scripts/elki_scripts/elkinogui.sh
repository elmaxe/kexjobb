#!/bin/sh
exec java -Xmx12G -Xms12G -cp "elki/elki-0.7.5.jar:elki/*:dependency/*" de.lmu.ifi.dbs.elki.application.KDDCLIApplication "$@"