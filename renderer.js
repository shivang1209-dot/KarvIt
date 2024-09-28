const { ipcRenderer } = require('electron');

// Button: Install Win32DiskImager
document.getElementById('installButton').addEventListener('click', () => {
  ipcRenderer.invoke('install-win32diskimager').then((response) => {
    document.getElementById('installStatus').innerText = response;
  }).catch((error) => {
    document.getElementById('installStatus').innerText = `Error: ${error}`;
  });
});

// Button: Verify Win32DiskImager
document.getElementById('browseButton').addEventListener('click', () => {
  ipcRenderer.invoke('verify-win32diskimager').then((response) => {
    alert(response);
  }).catch((error) => {
    alert(`Error: ${error}`);
  });
});

// Button: Create Disk Image
document.getElementById('createImageButton').addEventListener('click', () => {
  const driveName = document.getElementById('driveEntry').value;

  if (driveName) {
    ipcRenderer.invoke('create-disk-image', driveName).then((response) => {
      alert(response);
    }).catch((error) => {
      alert(`Error: ${error}`);
    });
  } else {
    alert('Please enter a drive name.');
  }
});

// Button: Go to File Carver
document.getElementById('goToCarverButton').addEventListener('click', () => {
  document.getElementById('main-container').style.display = 'none';
  document.getElementById('file-carver-container').style.display = 'block';
});

// Button: Back to Main Page
document.getElementById('backButton').addEventListener('click', () => {
  document.getElementById('file-carver-container').style.display = 'none';
  document.getElementById('main-container').style.display = 'block';
});

// Button: Start Carving
document.getElementById('startCarvingButton').addEventListener('click', () => {
  
  const image_path = document.getElementById('DiskImagePath').value;
  const fileType = document.getElementById('fileTypeDropdown').value;
  
  if (image_path){
    ipcRenderer.invoke('start-file-carving', image_path, fileType).then((response) => {
      alert(response);
    }).catch((error) => {
      alert(`Error: ${error}`);
    });
  } else {
    alert('Please select a file type to carve.');
  }
});

document.getElementById('disk_image').addEventListener('click', () => {
  document.getElementById('file-carver-container').style.display = 'none';
  document.getElementById('main-container').style.display = 'block';
});

document.getElementById('file_carve').addEventListener('click', () => {
  document.getElementById('file-carver-container').style.display = 'none';
  document.getElementById('main-container').style.display = 'block';
});