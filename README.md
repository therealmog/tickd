<img src="logo//blackBGLogo.png">
<h1>Tickd: task management made easy</h1>

<p>This is the repository for all the stuff to do with my A2 Project, Tickd.</p>
<br>

<h2>The <b>lib</b> folder</h2>
<p>Contains all the smaller processes, such as <a href="lib//getWallpaper.py">getWallpaper</a> (getting a random wallpaper), <a href="lib//getDetails.py">getDetails</a> [for all json handling], and my own created widgets, such as <a href="lib//checkbox_customTk.py">checkbox</a> and <a href="lib//submitBtn.py">submitBtn</a>.</p>
<br>

<h2>The structure</h2>
<p>Every 'page' in the app is its own class instance. For example, the authentication screen is first declared in the main program as the object named "auth".<br>This makes it very easy to quickly get values entered in one screen and then pass them onto a another screen.</p>