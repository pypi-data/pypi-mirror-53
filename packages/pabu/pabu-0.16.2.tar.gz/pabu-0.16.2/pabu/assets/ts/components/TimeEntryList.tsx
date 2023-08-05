import { Button, Link } from '@material-ui/core';
import * as React from 'react';
import StopWatch from '../containers/StopWatch';
import { formatDuration } from '../tools';
import { ExpandedTimeEntry, IssueStatus, Tag, TickingStat, TimeEntry } from '../types';
import PabuTable, { TableColDesriptor } from './PabuTable';
import moment = require('moment');
import MultiSelect from './MultiSelect';

export type OwnProps = {
    id: number,
}

export type StateProps = {
    rows: Array<ExpandedTimeEntry>,
    tickingStat: TickingStat,
    tags: Array<Tag>,
}

export type DispatchProps = {
    onDelete: (entry: ExpandedTimeEntry) => void,
    onAddNewTime: (projectId: number) => void,
    onStartTime: (projectId: number) => void,
    onStopTime: () => void,
    showIssue: (id: number) => void,
}

const renderIssueLink = (entry: ExpandedTimeEntry, showIssue): React.ReactNode => {
    const textDecoration = entry.issueStatus == IssueStatus.DONE ? 'line-through' : 'initial'
    return <Link style={{cursor: 'pointer', textDecoration}} onClick={() => showIssue(entry.issueId)}>#{entry.issueId}</Link>
}

export default ((props: StateProps & DispatchProps & OwnProps) => {
    const {tickingStat, rows, onDelete, onAddNewTime, onStartTime, onStopTime, id, showIssue, tags} = props;

    const lengthFormatter = (v: number, entry: TimeEntry) => entry.end ? formatDuration(v) : <StopWatch projectId={id} initialValue={v} />

    const [tagFilter, setTagFilter] = React.useState<Array<number>>([]);

    const rowDescriptors = [
        new TableColDesriptor('start', 'Start', v => moment.unix(v).format('YYYY-MM-DD HH:mm')),
        new TableColDesriptor('spentHours' , 'Length', lengthFormatter),
        new TableColDesriptor<ExpandedTimeEntry>('issueId', 'Task', (id, entry) => id ? renderIssueLink(entry, showIssue) : null),
        new TableColDesriptor('userName', 'User'),
    ]

    let tickingButton = <Button size="small" disabled>Start</Button>;
    if (tickingStat.ticking) {
        if (tickingStat.entry.projectId == id)
            tickingButton = <Button size="small" color="secondary" variant="contained" onClick={onStopTime}>Stop</Button>
    } else
        tickingButton = <Button size="small" color="primary" onClick={onStartTime.bind(this, id)}>Start</Button>

    const controllCellHeader = <div>
        {tickingButton}
        <Button size="small" color="primary" onClick={onAddNewTime.bind(this, id)}>Add</Button>
    </div>

    const filteredRows = tagFilter.length ? rows.filter(r => r.issueTags.filter(id => tagFilter.includes(id)).length == tagFilter.length) : rows;

    function timeSum(data: Array<ExpandedTimeEntry>): number {
        return data.reduce((prev, curr) => prev + curr.spentHours, 0);
    }

    const timeStat = {
        allSpent: formatDuration(timeSum(rows)),
        filteredSpent: formatDuration(timeSum(filteredRows)),
    };

    return (
        <React.Fragment>
            <div style={{padding: 10, display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <div style={{flexGrow: 1}}>
                    <MultiSelect
                        label="Issue tag filter"
                        placeholder="Select tags for issue filter"
                        options={tags.map(t => ({label: t.name, value: t.id}))}
                        values={tags.filter(t => tagFilter.includes(t.id)).map(t => ({label: t.name, value: t.id}))}
                        onChange={v => setTagFilter(v.map(v => v.value))}
                    />
                </div>
                <div style={{marginLeft: 10}}>
                    Time spent summary:<br/>
                    {timeStat.filteredSpent}
                    {timeStat.allSpent != timeStat.filteredSpent ? (<span> / {timeStat.allSpent}</span>) : ''}
                </div>
             </div>
            <PabuTable colDescriptors={rowDescriptors} rows={filteredRows} onDelete={onDelete} controllCellHeader={controllCellHeader} />
        </React.Fragment>
    )
})
