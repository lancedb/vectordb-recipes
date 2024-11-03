let selectedModel = 'gpt-4'; // default value
let fileName = ""

// Function to set the selected model
export const setSelectedModelInStore = (model) => {
  selectedModel = model;
};

// Function to get the selected model
export const getSelectedModel = () => {
  return selectedModel;
};

export const setFileName = (name) => {
  fileName = name;
};

// Function to get the selected model
export const getFileName = () => {
  return fileName;
};