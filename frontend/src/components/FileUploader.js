// src/components/FileUploader.js
import React from 'react';
import { Card, Button, Spin, message } from 'antd';
import DragAndDrop from './DragAndDrop';
import useFileSelection from '../hooks/useFileSelection';
import api from '../services/api';
import '../styles/FileUploader.css'; // Import the CSS file

const FileUploader = () => {
  const [addFile, removeFile, selectedFiles] = useFileSelection();
  const [loading, setLoading] = React.useState(false);

  const handleSubmit = async () => {
    if (selectedFiles.length === 0) {
      message.error('Please upload at least one PDF file.');
      return;
    }

    setLoading(true);
    try {
      await api.uploadFiles(selectedFiles);
      message.success('Files uploaded successfully');
    } catch (error) {
      message.error('Failed to upload files: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      className="file-uploader-card"
      actions={[
        <Button
          className="file-uploader-button"
          type="primary"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? <Spin /> : 'Submit'}
        </Button>,
      ]}
    >
      <DragAndDrop 
        addFile={addFile} 
        removeFile={removeFile} 
        selectedFiles={selectedFiles} // Passing selectedFiles as a prop
      />
    </Card>
  );
};

export default FileUploader;
