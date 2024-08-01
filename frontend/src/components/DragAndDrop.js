// src/components/DragAndDrop.js
import React from 'react';
import { Upload } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useDropzone } from 'react-dropzone';
import useFilePreview from '../hooks/useFilePreview';

const { Dragger } = Upload;

const DragAndDrop = ({ addFile, removeFile }) => {
  const [handlePreview, previewContent] = useFilePreview();
  const [selectedFiles, setSelectedFiles] = React.useState([]);
  const onDrop = (acceptedFiles) => {
    acceptedFiles.forEach(addFile);
    setSelectedFiles([...selectedFiles, ...acceptedFiles]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <>
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <p>Drag 'n' drop some files here, or click to select files</p>
        )}
      </div>
      <Dragger
        multiple={true}
        onRemove={(file) => removeFile(file.originFileObj)}
        showUploadList={true}
        listType="picture-card"
        beforeUpload={(file) => {
          addFile(file);
          return false;
        }}
        onPreview={handlePreview}
      >
        <p className="ant-upload-drag-icon">
          <PlusOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
      </Dragger>
      {previewContent}
    </>
  );
};

export default DragAndDrop;
