import { useState, useEffect, useCallback } from 'react';

type ReadableStreamState<T> = {
    data: T[];
    loading: boolean;
    error: Error | null;
};

const useProgressiveReadableStream = <T>(
    getStream: (params?: object) => Promise<ReadableStream<T>>,
    params?: object
): ReadableStreamState<T> => {

    const [list, setList] = useState<T[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetchStreamData = useCallback(async () => {
        try {
            const stream = await getStream(params);
            const reader = stream.getReader();

            let result: T[] = [];

            while(true) {
                const {done, value} = await reader.read();
                if (done) { break; }
                result = [...result, value];
                setList(result);
            }

            reader.releaseLock();
            setLoading(false);
        } catch (error) {
            setError(error as Error);
            setLoading(false);
        }

    }, [getStream, params]);

    useEffect(() => {
        fetchStreamData();
    }, [fetchStreamData]);

    return { data: list, loading, error };

};

export default useProgressiveReadableStream;