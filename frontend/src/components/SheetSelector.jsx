import React from 'react';
import { ChevronDown } from 'lucide-react';

const SheetSelector = ({ sheets, selectedSheet, onChange, label }) => {
    return (
        <div className="flex flex-col gap-1 w-full max-w-xs">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">{label}</span>
            <div className="relative">
                <select
                    value={selectedSheet}
                    onChange={(e) => onChange(e.target.value)}
                    className="w-full appearance-none bg-gray-800 border border-gray-600 text-white py-2 px-3 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-700 focus:border-purple-500 transition-colors"
                >
                    {sheets.map((sheet) => (
                        <option key={sheet} value={sheet}>
                            {sheet}
                        </option>
                    ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-400">
                    <ChevronDown className="w-4 h-4" />
                </div>
            </div>
        </div>
    );
};

export default SheetSelector;
