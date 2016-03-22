# -*- coding: utf-8 -*-
##############################################################################
# 
# Project   : Defensor
# Author    : Yy
# Email     : yangwanyuan@ztgame.com
# Date      : 2015.11 
#
##############################################################################

conf_template="""God.watch do |w|
    w.name = "%s"
    w.start = "%s"
    w.stop = "%s"
    w.restart = "%s"
    #w.keepalive(:memory_max => 150.megabytes,
    #            :cpu_max => 50.percent)

    w.pid_file = "%s"
    w.start_if do |start|
      start.condition(:process_running) do |c|
        c.interval = 5.seconds
        c.running = false
      end
    end

    w.lifecycle do |on|
      on.condition(:flapping) do |c|
        c.to_state = [:start, :restart]
        c.times = 5
        c.within = 5.minute
        c.transition = :unmonitored
        #c.retry_in = 10.minutes
        #c.retry_times = 5
        #c.retry_within = 2.hours
      end
    end
end
"""