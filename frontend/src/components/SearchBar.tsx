import React from 'react';
import {
  TextField,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Button,
  Box,
} from '@mui/material';

interface SearchBarProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  searchType: string;
  setSearchType: (type: string) => void;
  handleSearch: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  searchQuery,
  setSearchQuery,
  searchType,
  setSearchType,
  handleSearch,
}) => {
  return (
    <Box
      component="form"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
        marginBottom: 4,
      }}
      onSubmit={(e) => {
        e.preventDefault();
        handleSearch();
      }}
    >
      <TextField
        fullWidth
        label="Search logs..."
        variant="outlined"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <FormControl component="fieldset">
        <FormLabel component="legend">Search Type</FormLabel>
        <RadioGroup
          row
          aria-label="search-type"
          name="search-type-group"
          value={searchType}
          onChange={(e) => setSearchType(e.target.value)}
        >
          <FormControlLabel value="keyword" control={<Radio />} label="Keyword" />
          <FormControlLabel value="semantic" control={<Radio />} label="Semantic" />
          <FormControlLabel value="hybrid" control={<Radio />} label="Hybrid" />
        </RadioGroup>
      </FormControl>
      <Button type="submit" variant="contained" color="primary">
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;