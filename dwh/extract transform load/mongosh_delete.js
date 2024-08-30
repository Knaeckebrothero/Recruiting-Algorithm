/*
This script deletes documents from the experiences_before collection
 based on the original_doc_id and title fields.

 Keep in mind that the original_doc_id and title fields should be indexed properly!
 otherwise, this trash will take forever to execute...
*/

// Fetch all documents from experiences_processed
const processedDocs = db.experiences_processed.find({}, {original_doc_id: 1, title: 1}).toArray();

// Construct a list of conditions to match documents in experiences_before
const conditions = processedDocs.map(doc => ({
    original_doc_id: doc.original_doc_id,
    title: doc.title
}));

// If conditions are not empty, delete documents from experiences_before
if (conditions.length > 0) {
    db.experiences_before.deleteMany({
        $or: conditions
    });
} else {
    print("No documents to delete based on the provided conditions.");
}
