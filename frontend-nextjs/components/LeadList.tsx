import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LeadList = () => {
  const [leads, setLeads] = useState<any[]>([]);

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const response = await axios.get('/api/v1/leads');
        setLeads(response.data.leads);
      } catch (error) {
        console.error(error);
      }
    };

    fetchLeads();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Leads</h2>
      <ul className="mt-4 list-disc pl-5">
        {leads.map((lead, index) => (
          <li key={index}>
            {lead.company_name}, {lead.country}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LeadList;