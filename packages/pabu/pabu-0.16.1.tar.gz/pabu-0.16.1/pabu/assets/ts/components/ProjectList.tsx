
import * as React from 'react';
import { TimeDialogContext, UserMap, PaymentSubmitData, Project, IssueDialogContext, Issue, IssueStatus, IssueFormData } from '../types';
import ProjectRow from '../components/ProjectRow';
import TimeEntryDialog from '../components/TimeEntryDialog';
import PaymentDialog from '../components/PaymentDialog';
import IssueFormDialog from './IssueFormDialog';

export type StateProps = {
    issueDialogContext: IssueDialogContext
    addTimeDialogContext: TimeDialogContext,
    openedProjectId: number,
    paymentDialogProjectId: number,
    projects: Array<Project>,
    users: UserMap,
    issueData: IssueFormData,
    tags: Array<string>,
}

export type DispatchProps = {
    closeProject: Function,
    hideAddIssueDialog: () => void,
    hideAddTimeDialog: () => void,
    hidePaymentDialog: () => void,
    onIssueSubmit: (name: string, desc: string, status: IssueStatus, projectId: number, id: number, tags: Array<string>) => void,
    onPaymentSubmit: (projectId: number, data: PaymentSubmitData) => void
    onTimeSubmit: (amount: string, time: string, projectId: number, issueId: number) => void,
    openProject: (id: number) => void,
    onHoverTitle: (projectId: number) => void,
}

export default React.memo((props: StateProps & DispatchProps) => {

    return <div>
                <IssueFormDialog
                    onSubmit={(name, desc, status, tags) => props.onIssueSubmit(name, desc, status, props.issueDialogContext.projectId, props.issueDialogContext.id, tags)}
                    opened={props.issueDialogContext != null}
                    initialData={props.issueData}
                    tags={props.tags}
                    onClose={props.hideAddIssueDialog} />
                <TimeEntryDialog
                    opened={props.addTimeDialogContext != null}
                    onSubmit={(amount, time) => props.onTimeSubmit(amount, time, props.addTimeDialogContext.projectId, props.addTimeDialogContext.issueId)}
                    onClose={props.hideAddTimeDialog}
                />
                <PaymentDialog
                    users={props.paymentDialogProjectId ? Object.values(props.users) : []}
                    opened={props.paymentDialogProjectId != null}
                    onSubmit={props.onPaymentSubmit.bind(this, props.paymentDialogProjectId)}
                    onClose={props.hidePaymentDialog}
                />
        <div style={{ marginTop: 20 }}>{
            props.projects.map(project => <ProjectRow
                key={project.id}
                project={project}
                onHoverTitle={props.onHoverTitle.bind(this, project.id)}
                expanded={project.id == props.openedProjectId}
                handleChange={id => {
                    if (id == props.openedProjectId)
                        props.closeProject();
                    else
                        props.openProject(id);
                }}
            />)
        }</div>
    </div>
});
