import * as React from 'react';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl, Input,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Theme,
    createStyles,
    withStyles,
    WithStyles,
} from '@material-ui/core';
import {IssueStatus, IssueFormData} from '../types';
import {DialogTransition} from './tools';
import MultiSelect from "./MultiSelect";

type State = IssueFormData;

const styles = () => createStyles({
    dialog: {
        overflow: 'visible',
    }
});

type Props = {
    opened: boolean,
    onSubmit: (name: string, desc: string, status: IssueStatus, tags: Array<string>) => void,
    initialData: State,
    onClose: () => void,
    tags: Array<string>,
} & WithStyles<typeof styles>;

class IssueFormDialog extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props);
        this.state = props.initialData;
    }

    componentWillReceiveProps(props: Props) {
        this.setState(props.initialData)
    }

    onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        this.submit();
    };

    submit = () => {
        this.props.onSubmit(this.state.name, this.state.desc, this.state.status, this.state.tags);
    }

    render() {
        let {name, desc, tags} = this.state;
        return <Dialog
            open={this.props.opened}
            onClose={this.props.onClose}
            aria-labelledby="form-dialog-title"
            TransitionComponent={DialogTransition}
            classes={{ paperScrollPaper: this.props.classes.dialog }}
        >
            <DialogTitle id="form-dialog-title">Create task</DialogTitle>
            <form onSubmit={this.onSubmit} id="create_project_form">
            <DialogContent className={this.props.classes.dialog}>
                <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Summary"
                    type="text"
                    required
                    value={name || ''}
                    onChange={ev => {
                        this.setState({name: ev.target.value})
                    }}
                    fullWidth
                />
                <FormControl fullWidth required>
                    <InputLabel htmlFor="status">Status</InputLabel>
                    <Select
                        margin="dense"
                        inputProps={{name: 'status', id: 'status'}}
                        onChange={ev => {
                            this.setState({status: ev.target.value as IssueStatus})
                        }}
                        value={this.state.status}
                    >
                        {Object.values(IssueStatus).map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                    </Select>
                </FormControl>
                <TextField
                    margin="dense"
                    id="description"
                    label="Description"
                    type="text"
                    value={desc || ''}
                    multiline
                    onChange={ev => {
                        this.setState({desc: ev.target.value})
                    }}
                    fullWidth
                />
                <MultiSelect
                    creatable
                    label="Tags"
                    values={tags.map(t => ({label: t, value: t}))}
                    options={this.props.tags.map(t => ({label: t, value: t}))}
                    onChange={v => this.setState({tags: v.map(t => t.value)})}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={this.props.onClose} color="primary">
                    Cancel
                </Button>
                <Button type="submit" color="primary">Submit</Button>
            </DialogActions>
            </form>
        </Dialog>
    }
}

export default withStyles(styles)(IssueFormDialog);
