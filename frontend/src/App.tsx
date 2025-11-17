import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  CssBaseline,
  Box,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import SearchBar from './components/SearchBar';
import LogList from './components/LogList';

// Define a basic theme
const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

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

function App() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('keyword');

  const fetchLogs = async () => {
    const url = new URL('http://localhost:8000/search');
    url.searchParams.append('query', searchQuery);
    url.searchParams.append('search_type', searchType);

    try {
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setLogs(data);
    } catch (error) {
      console.error('Error fetching logs:', error);
      setLogs([]); // Clear logs on error
    }
  };

  // Initial fetch for all logs
  useEffect(() => {
    fetchLogs();
  }, []);

  const handleSearch = () => {
    fetchLogs();
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Audit Log Viewer
          </Typography>
          <SearchBar
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            searchType={searchType}
            setSearchType={setSearchType}
            handleSearch={handleSearch}
          />
          <LogList logs={logs} />
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;