import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import SheetSelector from './SheetSelector';
import SpreadsheetGrid from './SpreadsheetGrid';
import { ArrowRightLeft, Settings, RefreshCw } from 'lucide-react';

const SxSView = ({ files, comparisonData, onBack }) => {
    const [sheets1, setSheets1] = useState([]);
    const [sheets2, setSheets2] = useState([]);

    const [selectedSheet1, setSelectedSheet1] = useState('');
    const [selectedSheet2, setSelectedSheet2] = useState('');

    const [data1, setData1] = useState(null);
    const [data2, setData2] = useState(null);

    const [highlightMap1, setHighlightMap1] = useState({});
    const [highlightMap2, setHighlightMap2] = useState({});

    const scrollRef1 = useRef(null);
    const scrollRef2 = useRef(null);
    const [selectedCell, setSelectedCell] = useState(null);
    const isSyncing = useRef(false);
    const [error, setError] = useState(null);

    // Process Comparison Data
    useEffect(() => {
        if (comparisonData && comparisonData.changes) {
            const map = {};
            comparisonData.changes.forEach(change => {
                const key = `${change.row}_${change.col}`;
                map[key] = change.type;
            });
            setHighlightMap1(map);
            setHighlightMap2(map);
        }
    }, [comparisonData]);

    // Fetch Sheet Names on Mount
    useEffect(() => {
        const fetchSheets = async () => {
            try {
                const res1 = await axios.get(`/api/sheets/${files.file1}`);
                const res2 = await axios.get(`/api/sheets/${files.file2}`);
                setSheets1(res1.data.sheets);
                setSheets2(res2.data.sheets);
                if (res1.data.sheets.length > 0) setSelectedSheet1(res1.data.sheets[0]);
                if (res2.data.sheets.length > 0) setSelectedSheet2(res2.data.sheets[0]);
                setError(null);
            } catch (err) {
                console.error("Error fetching sheets", err);
                setError("Failed to load sheets. Is the backend running? " + (err.response?.data?.detail || err.message));
            }
        };
        if (files.file1 && files.file2) fetchSheets();
    }, [files]);

    // Fetch Data for File 1
    useEffect(() => {
        const fetchData = async () => {
            if (!files.file1 || !selectedSheet1) return;
            try {
                const res = await axios.get(`/api/data/${files.file1}/${selectedSheet1}`);
                setData1(res.data);
            } catch (err) {
                console.error("Error fetching data 1", err);
            }
        };
        fetchData();
    }, [files.file1, selectedSheet1]);

    // Fetch Data for File 2
    useEffect(() => {
        const fetchData = async () => {
            if (!files.file2 || !selectedSheet2) return;
            try {
                const res = await axios.get(`/api/data/${files.file2}/${selectedSheet2}`);
                setData2(res.data);
            } catch (err) {
                console.error("Error fetching data 2", err);
            }
        };
        fetchData();
    }, [files.file2, selectedSheet2]);

    // Sync Scrolling with Ref (better performance than state)
    const handleScroll = (sourceRef, targetRef) => {
        if (isSyncing.current) return;
        isSyncing.current = true;
        if (targetRef.current && sourceRef.current) {
            targetRef.current.scrollTop = sourceRef.current.scrollTop;
            targetRef.current.scrollLeft = sourceRef.current.scrollLeft;
        }
        setTimeout(() => { isSyncing.current = false; }, 10);
    };

    const handleCellClick = (row, col) => {
        setSelectedCell({ row, col });
    };

    return (
        <div className="w-full h-screen flex flex-col bg-gray-950 text-white overflow-hidden">
            {/* Toolbar */}
            <div className="h-16 border-b border-gray-800 bg-gray-900 flex items-center justify-between px-4 shrink-0">
                <div className="flex items-center gap-4">
                    <button onClick={onBack} className="text-gray-400 hover:text-white">
                        <ArrowRightLeft className="w-5 h-5" />
                    </button>
                    <h1 className="font-bold text-lg tracking-tight">Side-by-Side View</h1>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                        <div className="w-3 h-3 bg-red-900/50 border border-red-500 rounded"></div> Modified
                    </div>
                    <button className="p-2 hover:bg-gray-800 rounded-full transition-colors">
                        <Settings className="w-5 h-5 text-gray-400" />
                    </button>
                </div>
            </div>

            {/* Main Content Split */}
            <div className="flex-1 flex overflow-hidden">
                {/* Left Panel */}
                <div className="flex-1 flex flex-col border-r border-gray-800 relative">
                    <div className="p-3 bg-gray-900/50 border-b border-gray-800 flex justify-between items-center">
                        <SheetSelector
                            sheets={sheets1}
                            selectedSheet={selectedSheet1}
                            onChange={setSelectedSheet1}
                            label="Original File"
                        />
                    </div>
                    <div className="flex-1 p-2 overflow-hidden">
                        <SpreadsheetGrid
                            data={data1}
                            highlightMap={highlightMap1}
                            scrollRef={scrollRef1}
                            onScroll={() => handleScroll(scrollRef1, scrollRef2)}
                            selectedCell={selectedCell}
                            onCellClick={handleCellClick}
                        />
                    </div>
                </div>

                {/* Right Panel */}
                <div className="flex-1 flex flex-col relative">
                    <div className="p-3 bg-gray-900/50 border-b border-gray-800 flex justify-between items-center">
                        <SheetSelector
                            sheets={sheets2}
                            selectedSheet={selectedSheet2}
                            onChange={setSelectedSheet2}
                            label="Modified File"
                        />
                    </div>
                    <div className="flex-1 p-2 overflow-hidden">
                        <SpreadsheetGrid
                            data={data2}
                            highlightMap={highlightMap2}
                            scrollRef={scrollRef2}
                            onScroll={() => handleScroll(scrollRef2, scrollRef1)}
                            selectedCell={selectedCell}
                            onCellClick={handleCellClick}
                        />
                    </div>
                </div>
            </div>
            {/* Debug Info */}
            <div className="bg-gray-900 border-t border-gray-800 p-2 text-xs text-gray-500 font-mono">
                DEBUG: File1={files.file1} (Sheets: {sheets1.length}) | File2={files.file2} (Sheets: {sheets2.length}) | Error: {error || 'None'}
            </div>
        </div>
    );
};

export default SxSView;
