// Query to extract experiences from the original collection and store them in a new collection.
[
  {
    $match: {
      experiences: {
        $ne: []
      }
    }
  },
  {
    $unwind: "$experiences"
  },
  {
    $project: {
      _id: 0,
      original_doc_id: {
        $toString: "$_id"
      },
      starts_at: "$experiences.starts_at",
      ends_at: "$experiences.ends_at",
      company: "$experiences.company",
      company_linkedin_profile_url:
        "$experiences.company_linkedin_profile_url",
      title: "$experiences.title",
      description: "$experiences.description",
      location: "$experiences.location",
      logo_url: "$experiences.logo_url"
    }
  },
  {
    $out: "new_experiences_collection"
  }
]
