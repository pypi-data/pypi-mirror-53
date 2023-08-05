
import { connect } from 'react-redux';
import { deleteTimeEntry, fetchProjects, openAddTimeDialog, startTime, stopTime, openIssueViewDialog, openConfirmDialog } from '../actions';
import TimeEntryList, { DispatchProps, OwnProps, StateProps } from '../components/TimeEntryList';
import { ExpandedTimeEntry, State, ThunkDispatcher, IssueStatus } from '../types';

function mapStateToProps(state: State, props: OwnProps): StateProps {
    const {issues, timeEntries, users, tickingStat, tags} = state;

    let entries = [];
    for (const id in timeEntries) {
        const entry = timeEntries[id];
        if (entry.projectId != props.id)
            continue


        const issue = (entry.issueId in issues) ? issues[entry.issueId] : null;

        let exEntry: ExpandedTimeEntry = {
            ...entry,
            issueStatus: issue ? issue.status : IssueStatus.TODO,
            issueName: issue ? issue.name : '',
            userName: (entry.userId in users) ? users[entry.userId].name : '',
            spentHours: (entry.end || new Date().getTime()/1000) - entry.start,
            issueTags: issue ? Object.values(tags).filter(t => issue.tags.includes(t.id)).map(t => t.id) : [],
        }
        entries.push(exEntry)
    }

    return {
        rows: entries,
        tickingStat,
        tags: Object.values(tags).filter(t => t.projectId == props.id),
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher): DispatchProps => {
    return {
        showIssue: (id: number) => dispatch(openIssueViewDialog(id)),
        onDelete: (entry: ExpandedTimeEntry) => {
            dispatch(openConfirmDialog({
                message: 'Do you really want to delete this time entry?',
                callback: () => dispatch(deleteTimeEntry(entry.id)).then(() => dispatch(fetchProjects(entry.projectId))),
            }))
        },
        onAddNewTime: (projectId) => dispatch(openAddTimeDialog(projectId)),
        onStartTime: (projectId: number) => dispatch(startTime(projectId)),
        onStopTime: () => dispatch(stopTime()),
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(TimeEntryList);
