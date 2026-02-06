import React from 'react';

const SpreadsheetGrid = ({ data, highlightMap, scrollRef, onScroll, selectedCell, onCellClick }) => {
    if (!data || !data.data) return <div className="p-4 text-gray-500">No data loaded</div>;

    const { rows, cols, data: gridData } = data;

    // ... (header logic remains same or duplicated briefly for context)
    const renderHeader = () => {
        return (
            <tr>
                <th className="sticky top-0 left-0 z-20 bg-gray-900 border-b border-r border-gray-700 w-12 h-8"></th>
                {Array.from({ length: cols }).map((_, i) => (
                    <th key={i} className={`sticky top-0 z-10 border-b border-r border-gray-700 px-2 py-1 text-xs font-medium min-w-[100px] ${selectedCell?.col === i ? 'bg-indigo-900/50 text-indigo-200' : 'bg-gray-800 text-gray-400'}`}>
                        {String.fromCharCode(65 + i)}
                    </th>
                ))}
            </tr>
        );
    };

    return (
        <div
            className="overflow-auto max-h-full h-full border border-gray-700 rounded-lg bg-gray-900 shadow-inner"
            ref={scrollRef}
            onScroll={onScroll}
        >
            <table className="border-collapse w-full relative">
                <thead className="sticky top-0 z-20">
                    {renderHeader()}
                </thead>
                <tbody>
                    {gridData.map((row, rIdx) => (
                        <tr key={rIdx}>
                            {/* Row Index */}
                            <td className={`sticky left-0 z-10 border-b border-r border-gray-700 text-center text-xs font-mono w-12 select-none ${selectedCell?.row === rIdx ? 'bg-indigo-900/50 text-indigo-200' : 'bg-gray-800 text-gray-500'}`}>
                                {rIdx + 1}
                            </td>

                            {/* Cells */}
                            {row.map((cell, cIdx) => {
                                const key = `${rIdx}_${cIdx}`;
                                const changeType = highlightMap[key];
                                const isSelected = selectedCell?.row === rIdx && selectedCell?.col === cIdx;

                                let cellClass = "border-b border-r border-gray-800 px-2 py-1 text-sm whitespace-nowrap overflow-hidden max-w-[200px] truncate transition-colors duration-100 cursor-pointer";

                                // Base Color
                                if (isSelected) {
                                    cellClass += " bg-indigo-600 text-white outline outline-2 outline-indigo-400 z-10";
                                } else if (changeType === 'modified') {
                                    cellClass += " bg-yellow-900/30 text-yellow-200 font-semibold";
                                } else if (changeType === 'added') {
                                    cellClass += " bg-green-900/30 text-green-200 font-semibold";
                                } else if (changeType === 'removed') {
                                    cellClass += " bg-red-900/30 text-red-200 font-semibold";
                                } else {
                                    cellClass += " text-gray-300 hover:bg-gray-800";
                                }

                                return (
                                    <td
                                        key={cIdx}
                                        className={cellClass}
                                        title={cell}
                                        onClick={() => onCellClick(rIdx, cIdx)}
                                    >
                                        {cell}
                                    </td>
                                );
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default SpreadsheetGrid;
