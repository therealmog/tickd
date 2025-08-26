<img src="logo//blackBGLogo.png" width=500>
<h1>tickd. task management made easy.</h1>

<h3>This is the repository for my OCR A-Level Computer Science Project/Non-Exam Assessment.</h3>
<br><br>

<h2><u>🌐 QUICK LINKS</u></h2>

<h3>✨ Ideas to be added (<a href="ideas.md" target="_blank">GitHub</a>)
<br><br>
👨‍💻 Code submitted to OCR (<a href="https://github.com/therealmog/A2_Project/tree/335804a6c9aa72e6472663cad339ea22483fd33b" target="_blank">GitHub</a>)
<br><br>
📄 Project documentation submitted to OCR (<a href="https://drive.google.com/file/d/1bncJgfuthEGVeOWDF_zf7tUzepB3hU95/preview" target="_blank">Google Drive</a>)
</h3>

<h2><u></u></h2>
<br>
<br>

<h2>The <b>lib</b> folder</h2>
<p>Contains all the smaller processes, such as <a href="lib//getWallpaper.py">getWallpaper</a> (getting a random wallpaper), <a href="lib//getDetails.py">getDetails</a> [for all json handling], and my own created widgets, such as <a href="lib//checkbox_customTk.py">checkbox</a> and <a href="lib//submitBtn.py">submitBtn</a>.</p>
<br>

<h2>The structure</h2>
<p>Every 'page' in the app is its own class instance.<br>For example, the authentication screen is first declared in the main program as the object named "auth".<br><br>This makes it very easy to quickly get values entered in one screen and then pass them onto a another screen.</p>

<br>

<p>There are 3 main components to the application</p>
<ol>
  <h3><li>App window</li></h3>
  <ul>
    <li>Essentially the 'master' window of the app, acts as a container for the content frames of the app.</li>
    <li>Also contains a few functions used to refresh data, since this object will contain all of the frames of the app, allowing it to call any methods for any of those frames.</li>
  </ul>
  <img src="sample_imgs//appwindow.png" width=700>
  <h3><li>List frames</li></h3>
  <h3><li>Task objects</li></h3>
</ol>
