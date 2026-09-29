# Using Pylint:
To use Pylint, install the pylint extension from the marketplace
Pylint will autmatically show formatting errors in files
To view more complex errors in a file, you can run ( pylint "fileDirectory" )

# Run Pytest locally
.venv/bin/python -m pytest MachineLearning/Tests
- This should be run from the root directory

# Running Unity Build
Borrowed from [This Tutorial](https://www.codegenes.net/blog/how-do-i-run-a-local-unity-webgl-file-url-build/#nodejs-http-server):
1. Navigate to your Unity WebGL build folder in a terminal:
`cd /GildedGuild/frontend/public/WebGL` on Windows  

2. Start the server:

    Python 3.x:
    `python -m http.server 8000`

    Python 2.x (older systems):
    `python -m SimpleHTTPServer 8000`  

3. Open your browser and go to [http://localhost:8000](http://localhost:8000) your Unity build will load!