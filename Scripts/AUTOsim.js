

const rootCauseText = 'Optics - TT SOP not followed';
await issue.edit(
  {path: "/extensions/tt/rootCause", editAction: "PUT", data: rootCauseText},
  {path: "/extensions/tt/closureCode", editAction: "PUT", data: 'Unsuccessful'}
);





 !['a92e54ab-45c9-4acf-a957-6eddb3be7d28', 'a9515f77-2718-47be-a35b-41533bb7c315'].includes(_.get(issue, 'source.id'))




const ttCategory = "HVH MOR";
const ttType = "Configuration";
const ttItem = "Camera add/remove";
const ttResolver = "FR HVR Team";
const ttImpact = 3;



_.get(issue, 'extensions.tt.type') === 'Configuration'
_.get(issue, 'extensions.tt.item') === 'Camera add/remove'