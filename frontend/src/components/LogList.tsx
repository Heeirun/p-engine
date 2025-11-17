import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

interface TargetEntity {
  id: string;
  type: string;
}

interface Log {
  id: string;
  action: string;
  summary: string;
  description: string;
  ip_address: string;
  occured_at: string;
  created_at: string;
  actor_id: string;
  organization_id: string;
  target_entities: TargetEntity[];
}

interface LogListProps {
  logs: Log[];
}

const LogList: React.FC<LogListProps> = ({ logs }) => {
  return (
    <Box>
      {logs.length > 0 ? (
        logs.map((log) => (
          <Card key={log.id} sx={{ marginBottom: 2 }}>
            <CardContent>
              <Typography variant="h6" component="div">
                {log.summary}
              </Typography>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                Action: {log.action}
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                {log.description}
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="Timestamp"
                    secondary={new Date(log.occured_at).toLocaleString()}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText primary="IP Address" secondary={log.ip_address} />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Actor ID" secondary={log.actor_id} />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Organization ID"
                    secondary={log.organization_id}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        ))
      ) : (
        <Typography>No logs found.</Typography>
      )}
    </Box>
  );
};

export default LogList;