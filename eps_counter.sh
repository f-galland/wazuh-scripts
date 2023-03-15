#!/bin/bash

function getEventCount () {
        echo "$(grep -Po "(?<=msg_sent\=\')\d+" /var/ossec/var/run/wazuh-agentd.state)"
}

fede="$(getEventCount)"

while (true)
do
        previous_events="$(getEventCount)"
        sleep 1s
        current_events="$(getEventCount)"
        date=$(date)
        eps=$current_events-$previous_events
        echo -ne "$date\tEvents per second:\t$((eps))\n"
done

exit 0
