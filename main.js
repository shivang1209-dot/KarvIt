const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// IPC for installing Win32DiskImager
ipcMain.handle('install-win32diskimager', (event) => {
  return new Promise((resolve, reject) => {
    exec('python3 python/disk_imager.py --install', (error, stdout, stderr) => {
      if (error) {
        reject(stderr);
      } else {
        resolve(stdout);
      }
    });
  });
});

// IPC for verifying Win32DiskImager
ipcMain.handle('verify-win32diskimager', (event) => {
  return new Promise((resolve, reject) => {
    exec('python3 python/disk_imager.py --verify', (error, stdout, stderr) => {
      if (error) {
        reject(stderr);
      } else {
        resolve(stdout);
      }
    });
  });
});

// IPC for creating a disk image
ipcMain.handle('create-disk-image', (event, driveName) => {
  return new Promise((resolve, reject) => {
    exec(`python3 python/disk_imager.py --create-image ${driveName}`, (error, stdout, stderr) => {
      if (error) {
        reject(stderr);
      } else {
        resolve(stdout);
      }
    });
  });
});

// IPC for file carving
ipcMain.handle('start-file-carving', (event, image_path, fileType) => {
  return new Promise((resolve, reject) => {
    exec(`python3 python/file_carver.py --file ${image_path} --type ${fileType}`, (error, stdout, stderr) => {
      if (error) {
        reject(stderr);
      } else {
        resolve(stdout);
      }
    });
  });
});
