// src/components/DragAndDrop.js
import React from 'react';
import { Upload, Button } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { useDropzone } from 'react-dropzone';
import '../styles/DragAndDrop.css'; // Ensure the CSS is imported

const DragAndDrop = ({ addFile, removeFile }) => {
  const [selectedFiles, setSelectedFiles] = React.useState([]);

  const onDrop = (acceptedFiles) => {
    console.log('Accepted Files:', acceptedFiles);
    acceptedFiles.forEach((file) => {
      console.log('Adding file to current selection:', file.name);
      addFile(file);
    });

    setSelectedFiles((currentSelection) => [...currentSelection, ...acceptedFiles]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    // No accept parameter means accept all file types
  });

  return (
    <div className="drag-and-drop-container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p className="ant-upload-text">Drag 'n' drop some files here, or click to select files</p>
        <Button icon={<InboxOutlined />} size="large">Upload</Button>
      </div>
      {selectedFiles.length > 0 && (
        <Upload
          fileList={selectedFiles.map(file => ({
            uid: file.name,
            name: file.name,
            status: 'done',
            originFileObj: file
          }))}
          onRemove={(file) => {
            console.log('Removing file:', file.name);
            removeFile(file.originFileObj || file);
            setSelectedFiles((currentSelection) =>
              currentSelection.filter((f) => f.name !== file.name)
            );
          }}
          showUploadList={{
            showPreviewIcon: false,
            showRemoveIcon: true,
            showDownloadIcon: false
          }}
        />
      )}
    </div>
  );
};

export default DragAndDrop;
