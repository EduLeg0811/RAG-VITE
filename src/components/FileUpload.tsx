import React, { useCallback } from 'react';
import { Upload, X, FileText } from 'lucide-react';
import { UploadedFile } from '../types';

interface FileUploadProps {
  files: UploadedFile[];
  onFilesAdd: (files: UploadedFile[]) => void;
  onFileRemove: (fileId: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  files,
  onFilesAdd,
  onFileRemove
}) => {
  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || []);
    const validFiles = selectedFiles.filter(file => 
      file.type === 'text/plain' || 
      file.name.endsWith('.md') || 
      file.name.endsWith('.txt')
    );

    const uploadedFiles: UploadedFile[] = [];

    for (const file of validFiles) {
      const content = await file.text();
      uploadedFiles.push({
        id: `${Date.now()}_${Math.random()}`,
        name: file.name,
        content,
        processed: false
      });
    }

    onFilesAdd(uploadedFiles);
    event.target.value = '';
  }, [onFilesAdd]);

  return (
    <div className="file-upload-section">
      <h3><Upload className="icon" /> Upload de Documentos</h3>
      <p className="subtitle">Adicione arquivos .txt ou .md para criar bases de conhecimento</p>
      
      <div className="upload-area">
        <input
          type="file"
          multiple
          accept=".txt,.md"
          onChange={handleFileUpload}
          className="file-input"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="upload-label">
          <Upload className="icon" />
          Selecionar Arquivos
        </label>
      </div>

      {files.length > 0 && (
        <div className="uploaded-files">
          <h4>Arquivos Carregados:</h4>
          {files.map(file => (
            <div key={file.id} className="file-item">
              <div className="file-info">
                <FileText className="icon" />
                <span className="file-name">{file.name}</span>
                <span className={`file-status ${file.processed ? 'processed' : 'pending'}`}>
                  {file.processed ? '✅ Processado' : '⏳ Pendente'}
                </span>
              </div>
              <button
                onClick={() => onFileRemove(file.id)}
                className="remove-button"
                title="Remover arquivo"
              >
                <X className="icon" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};