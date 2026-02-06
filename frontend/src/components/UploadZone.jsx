import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileSpreadsheet, ArrowRight, Loader2 } from 'lucide-react';

const UploadZone = ({ onCompareResult }) => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e, setFile) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setError(null);
        }
    };

    const onDrop = (e, setFile) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
            setError(null);
        }
    };

    const onDragOver = (e) => {
        e.preventDefault();
    };

    const handleCompare = async () => {
        if (!file1 || !file2) {
            setError("Please select both files to compare.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // 1. Upload File 1
            const formData1 = new FormData();
            formData1.append('file', file1);
            const upload1 = await axios.post('/api/upload', formData1);

            // 2. Upload File 2
            const formData2 = new FormData();
            formData2.append('file', file2);
            const upload2 = await axios.post('/api/upload', formData2);

            // 3. Trigger Comparison
            const compareRes = await axios.post('/api/compare', {
                file1: upload1.data.filename,
                file2: upload2.data.filename
            });

            onCompareResult({
                data: compareRes.data,
                files: {
                    file1: upload1.data.filename,
                    file2: upload2.data.filename
                }
            });

        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || "An error occurred during comparison.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-semibold text-white mb-2">Start New Comparison</h2>
                <p className="text-gray-400">Select two Excel files to analyze differences</p>
            </div>

            <div className="flex flex-col md:flex-row gap-8 items-center justify-center mb-8">
                {/* File 1 Input */}
                <div className="w-full md:w-1/3">
                    <label
                        onDrop={(e) => onDrop(e, setFile1)}
                        onDragOver={onDragOver}
                        className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-gray-500 rounded-lg cursor-pointer hover:bg-gray-700 hover:border-blue-500 transition-all group"
                    >
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                            {file1 ? (
                                <>
                                    <FileSpreadsheet className="w-10 h-10 text-green-400 mb-2" />
                                    <p className="text-sm text-gray-200 font-medium truncate max-w-[200px]">{file1.name}</p>
                                </>
                            ) : (
                                <>
                                    <Upload className="w-10 h-10 text-gray-400 group-hover:text-blue-400 mb-2" />
                                    <p className="text-sm text-gray-400">Select Original File</p>
                                </>
                            )}
                        </div>
                        <input type="file" className="hidden" accept=".xlsx, .xls" onChange={(e) => handleFileChange(e, setFile1)} />
                    </label>
                </div>

                <ArrowRight className="hidden md:block text-gray-500 w-8 h-8" />

                {/* File 2 Input */}
                <div className="w-full md:w-1/3">
                    <label
                        onDrop={(e) => onDrop(e, setFile2)}
                        onDragOver={onDragOver}
                        className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-gray-500 rounded-lg cursor-pointer hover:bg-gray-700 hover:border-purple-500 transition-all group"
                    >
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                            {file2 ? (
                                <>
                                    <FileSpreadsheet className="w-10 h-10 text-purple-400 mb-2" />
                                    <p className="text-sm text-gray-200 font-medium truncate max-w-[200px]">{file2.name}</p>
                                </>
                            ) : (
                                <>
                                    <Upload className="w-10 h-10 text-gray-400 group-hover:text-purple-400 mb-2" />
                                    <p className="text-sm text-gray-400">Select Modified File</p>
                                </>
                            )}
                        </div>
                        <input type="file" className="hidden" accept=".xlsx, .xls" onChange={(e) => handleFileChange(e, setFile2)} />
                    </label>
                </div>
            </div>

            {error && (
                <div className="mb-6 p-4 bg-red-900/50 border border-red-700 text-red-200 rounded-lg text-sm text-center">
                    {error}
                </div>
            )}

            <div className="text-center">
                <button
                    onClick={handleCompare}
                    disabled={loading || !file1 || !file2}
                    className={`px-8 py-3 rounded-lg font-semibold text-white transition-all transform hover:scale-105 ${loading || !file1 || !file2
                        ? 'bg-gray-600 cursor-not-allowed'
                        : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg hover:shadow-purple-500/30'
                        }`}
                >
                    {loading ? (
                        <span className="flex items-center justify-center gap-2">
                            <Loader2 className="w-5 h-5 animate-spin" /> Analyzing...
                        </span>
                    ) : (
                        "Compare Files"
                    )}
                </button>
            </div>
        </div>
    );
};

export default UploadZone;
