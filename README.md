<img src="logo//blackBGLogo.png" width=500>
<h1>tickd. task management made easy.</h1>

<h3>To see stuff that could be added, see <a href="ideas.md">here</a>.</h3>
<h3>The project has been submitted, please see <a href="https://github.com/therealmog/A2_Project/tree/335804a6c9aa72e6472663cad339ea22483fd33b" target="_blank">here</a> to see the version of the code that was submitted to OCR, and see the project documentation <a href="https://drive.google.com/file/d/1bncJgfuthEGVeOWDF_zf7tUzepB3hU95/view?usp=sharing" target="_blank">here</a> (it was too big to put on GitHub!)</h3>

<iframe src="https://drive.google.com/file/d/1bncJgfuthEGVeOWDF_zf7tUzepB3hU95/preview" width="640" height="480" allow="autoplay"></iframe>
<p>This is the repository for all the stuff to do with my A Level Project, Tickd.</p>
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
