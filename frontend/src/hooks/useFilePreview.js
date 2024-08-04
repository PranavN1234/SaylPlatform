// src/hooks/useFilePreview.js
import { Modal, Typography } from 'antd';
import { useState } from 'react';

const useFilePreview = () => {
  const [previewVisibility, setPreviewVisibility] = useState(false);
  const [previewTitle, setPreviewTitle] = useState('');

  const handlePreview = async (file) => {
    setPreviewTitle(file.name);
    setPreviewVisibility(true);
  };

  const hidePreview = () => {
    setPreviewVisibility(false);
  };

  const previewContent = (
    <Modal
      visible={previewVisibility}
      title={previewTitle}
      footer={null}
      onCancel={hidePreview}
    >
      <Typography.Text>Preview not available for PDFs. File name: {previewTitle}</Typography.Text>
    </Modal>
  );

  return [handlePreview, previewContent];
};

export default useFilePreview;
