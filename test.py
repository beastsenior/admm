import curses,time

stdscr = curses.initscr()

# curses.noecho()
# curses.cbreak()
# stdscr.nodelay(1)
stdscr.addstr(5,0,'===============hello===========')
stdscr.refresh()
time.sleep(10)
curses.endwin()

