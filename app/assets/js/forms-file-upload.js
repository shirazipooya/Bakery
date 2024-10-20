/**
 * File Upload
 */

'use strict';

(function () {
  // previewTemplate: Updated Dropzone default previewTemplate
  // ! Don't change it unless you really know what you are doing
  const previewTemplate = `<div class="dz-preview dz-file-preview">
<div class="dz-details">
  <div class="dz-thumbnail">
    <img data-dz-thumbnail>
    <span class="dz-nopreview">No preview</span>
    <div class="dz-success-mark"></div>
    <div class="dz-error-mark"></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
    <div class="progress">
      <div class="progress-bar progress-bar-primary" role="progressbar" aria-valuemin="0" aria-valuemax="100" data-dz-uploadprogress></div>
    </div>
  </div>
  <div class="dz-filename" data-dz-name></div>
  <div class="dz-size" data-dz-size></div>
</div>
</div>`;

  // ? Start your code from here

  // Basic Dropzone
  // --------------------------------------------------------------------
  const dropzoneBasic = document.querySelector('#dropzone-basic');
  const uploadButton = document.querySelector('#upload-button');
  if (dropzoneBasic) {
    const myDropzone = new Dropzone(dropzoneBasic, {
      url: "/api/database/upload",  // Make sure this matches the Flask route
      method: "post",
      previewTemplate: previewTemplate,
      parallelUploads: 1,
      maxFilesize: 5,
      addRemoveLinks: true,
      maxFiles: 1,
      acceptedFiles: '.csv',
      // init: function() {
      //   this.on("addedfile", function(file) {
      //     uploadButton.disabled = false; // Enable the button when a file is added
      //   });
      //   this.on("removedfile", function(file) {
      //     if (this.files.length === 0) {
      //       uploadButton.disabled = true; // Disable the button if no files remain
      //     }
      //   });
      // },
      // success: function(file, response) {
      //   console.log('File uploaded successfully', response);
      //   // Optionally reset the Dropzone
      //   this.removeAllFiles();
      //   uploadButton.disabled = true; // Disable button again after upload
      // },
      // error: function(file, response) {
      //   console.error('Error uploading file', response);
      // }
    });
  }
  uploadButton.addEventListener('click', function() {
    dropzoneBasic.dropzone.processQueue(); // Trigger the upload process
  });
})();
