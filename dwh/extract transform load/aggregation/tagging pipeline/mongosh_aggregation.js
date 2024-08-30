// This aggregation is used to extract the distinct values from the processed experiences.
db.experiences_processed.aggregate([
    {
        $group: {
            _id: null,
            distinctIndustries: { $addToSet: "$industry" },
            distinctProfessions: { $addToSet: "$profession" }
        }
    },
    {
        $unwind: "$distinctIndustries"
    },
    {
        $unwind: "$distinctProfessions"
    },
    {
        $lookup: {
            from: "experiences_processed",
            pipeline: [
                { $unwind: "$skills" },
                { $group: { _id: null, distinctSkills: { $addToSet: "$skills" } } }
            ],
            as: "skillsData"
        }
    },
    {
        $lookup: {
            from: "experiences_processed",
            pipeline: [
                { $unwind: "$tags" },
                { $group: { _id: null, distinctTags: { $addToSet: "$tags" } } }
            ],
            as: "tagsData"
        }
    },
    {
        $project: {
            distinctIndustries: 1,
            distinctProfessions: 1,
            distinctSkills: { $arrayElemAt: ["$skillsData.distinctSkills", 0] },
            distinctTags: { $arrayElemAt: ["$tagsData.distinctTags", 0] }
        }
    }
]).toArray();
