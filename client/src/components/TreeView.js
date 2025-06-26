import "./TreeView.css";

// Libs
import React, { useState } from "react";

// 🔒 Kleines Icon-Komponent zur besseren Lesbarkeit
function ExpandCollapseIcon({ isExpanded, onClick }) {
    const iconArrow = isExpanded ? "icon-arrow-down" : "icon-arrow-right";

    return (
        <i
            onClick={onClick}
            className={`icon ${iconArrow} mr-1 cursor-pointer text-gray`}
        />
    );
}

function PlaceHolderIcon() {
    return <i className={`icon mr-1`} style={{ visibility: "hidden" }} />;
}

// 🔒 Checkbox + Label-Zeile
const TreeItemLabel = ({
    node,
    isChecked,
    onToggleChecked,
    hasChildren,
    expanded,
    onToggleExpand,
}) => (
    <div className="d-flex d-flex-vertical-center">
        {hasChildren ? (
            <ExpandCollapseIcon
                isExpanded={expanded}
                onClick={onToggleExpand}
            />
        ) : (
            <PlaceHolderIcon />
        )}
        <input
            className="mx-1 align-middle"
            type="checkbox"
            checked={isChecked}
            onChange={onToggleChecked}
        />
        <span className={`box ${isChecked ? " text-bold" : ""}`}>
            {node.label}
        </span>
    </div>
);

function TreeNode({ node }) {
    const [expanded, setExpanded] = useState(false);
    const [isChecked, setIsChecked] = useState(false);
    const hasChildren = node.children && node.children.length > 0;

    return (
        <li className="nav-item">
            <TreeItemLabel
                node={node}
                isChecked={isChecked}
                onToggleChecked={(e) => setIsChecked(e.target.checked)}
                hasChildren={hasChildren}
                expanded={expanded}
                onToggleExpand={() => setExpanded(!expanded)}
            />
            {hasChildren && expanded && (
                <ul className="nav">
                    {node.children.map((child) => (
                        <TreeNode key={child.id} node={child} />
                    ))}
                </ul>
            )}
        </li>
    );
}

function TreeView({ data }) {
    return (
        <div>
            <ul className="nav">
                {data.map((node) => (
                    <TreeNode key={node.id} node={node} />
                ))}
            </ul>
        </div>
    );
}

export default TreeView;
