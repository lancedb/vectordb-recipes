// Modal.js
import React from "react";
import FileUploader from "./fileUploader";  // Import FileUploader component
import { XMarkIcon } from '@heroicons/react/24/outline';  // Outline version


const FileUploaderModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;  // Don't render the modal if it's not open

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-1/3">
        <div className="flex justify-end -mt-4 -mr-5">
          <button className="text-black px-4 py-2 hover:bg-gray-300 rounded" onClick={onClose}>
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>
        <FileUploader onClose={onClose} />
      </div>
    </div>
  );
};

export default FileUploaderModal;
