// src/hooks/useFileSelection.js
import { useState } from 'react';

const useFileSelection = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const addFile = (file) => {
    setSelectedFiles((currentSelection) => {
      const newSelection = [...currentSelection, file];
      console.log('File added:', file.name);
      console.log('Current selection:', newSelection);
      return newSelection;
    });
  };

  const removeFile = (file) => {
    setSelectedFiles((currentSelection) => {
      const newSelection = currentSelection.slice();
      const fileIndex = currentSelection.indexOf(file);
      if (fileIndex !== -1) {
        newSelection.splice(fileIndex, 1);
        console.log('File removed:', file.name);
      }
      console.log('Current selection after removal:', newSelection);
      return newSelection;
    });
  };

  return [addFile, removeFile, selectedFiles];
};

export default useFileSelection;
