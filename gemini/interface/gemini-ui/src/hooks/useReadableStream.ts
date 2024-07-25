import { useQuery } from "@tanstack/react-query";
import { useCallback} from "react";

const useReadableStream = (
    queryKey: string,
    queryFn: (params?: object) => Promise<ReadableStream<any>>,
    params?: object
) => {
    const fetchStreamData = useCallback(async () => {
        // Call the query function to get the ReadableStream
        const stream = await queryFn(params);
        const records: any[] = []; // Array to store records
        const reader = stream.getReader(); // Get a reader for the stream

        while(true) {
            const {done, value} = await reader.read(); // Read the next value from the stream
            if (done) { break; } // If done, break the loop
            records.push(value); // Add the value to the records array
        }

        return records; // Return the records array
    }, [queryFn, params]);

    // Use the useQuery hook to fetch the data
    return useQuery({
        queryKey: [queryKey, params],
        queryFn: fetchStreamData,
    });
}

export default useReadableStream;