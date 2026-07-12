<h1>YARCoM</h1>
<div align="center">
    <img src="icons/YARCoM.by.faro340x233.png" alt="YARCoM" width="100%">  
</div>
This tool manages a list of remote devices to connect to using your favorite connection tool (ssh on Linux, PuTTY on MS OS, etc.).
<br>This tool is developped using Python and Qt pyside6 library. You can find the same tool using TCL/Tk, but less advanced, in another directory in my repository.  
<br>A keepass vault can be associated to retrieve passwords automatically.

<h2>Features</h2>
<ol><li>Only one configuration file (.json) describing the setup :</li>
<ul>
<li>A global configuration including:
    <ul>
    <li>Connection tools (SSH, SFTP, etc.)</li>
    <li>KeePass vaults</li>
    </ul>
</li>
</ul>
<ul>
<li>Connections are structured as following :
    <ul>
    <li>IP address</li>
    <li>Connection port</li>
    <li>Connection tool to use</li>
    <li>KeePass vault to use</li>
    <li>Username for retrieving the vault password</li>
    </ul>
</li>
</ul>

<li>All is done from the main window :</li>
    <ul>
    <li>Access to preferences window using <img src="icons/prefs.png" alt="Description" width="20" height="20">. There are two tabs :
        <ul>
        <li>One to configure the applications</li>
        <li>One to  configure the keepass vaults</li>
        <li>Exiting the window automatically save changes of both tabs</li>
        </ul>
    </li>
    <li>Create a sub-tree <img src="icons/add_folder.png" alt="Description" width="20" height="20"></li>
    <li>Create a connections <img src="icons/add_computer.png" alt="Description" width="20" height="20"></li>
    <li>Delete a sub-tree or a connection <img src="icons/trash.png" alt="Description" width="20" height="20"></li>
    <li>Selecting an item allow its modification :</li>
        <ul>
        <li>For a sub-tree, its name</li>
        <li>For a connection, all its structure, described previously</li>
        <li>Modification is saved by clicking <img src="icons/edit.png" alt="Description" width="20" height="20"></li>
        </ul>
    </li>
    </ul>

<li>Drag and drop in connections tree allow to reorder sub-trees and connections. All changes are saved automatically.</li>
<li>If one or many keepass are defined, each vault password is asked at startup (or when you configure one ... I guess &#x1F914;). Each password is encrypted in memory. None of them are saved in the configuration file. The vaults are used in conjunction with the username defined for each connection.</li>
</ol>  

## Installation

1. Clone this project :
```
$ git clone git@github.com:faro93/YARCoM.Qt
```
**N.B. :** _Be careful to configure your SSH token to be able to clone this repository._

2. Go to the directory and activate the virtual environment :
```
$ cd YARCoM.Qt/
$ python -m venv .venv
```
- For macOS and Linux : `$ source .venv/bin/activate`
- For Windows (cmd) : `.venv\Scripts\activate.bat`
- For Windows (PowerShell) : `.venv\Scripts\Activate.ps1`

3. Then install required python libraries :
```
$ pip install -r requirements.txt
```

## Usage
Run **YARCoM.py** :

```
./YARCoM.py
```
**N.B. :** _shebang script is configured with_ `#!/usr/bin/env python3`_, so it will run with your_ `venv` _installed python._

## Contributing
Me &#x1f601;

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License
[GPL](https://www.gnu.org/licenses/gpl-3.0.html)