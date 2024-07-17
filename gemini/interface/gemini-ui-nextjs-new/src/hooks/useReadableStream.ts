import { useEffect, useState } from 'react';

interface StreamState {
    data: any[];
    error: Error | null;
    loading: boolean;
}

const useReadableStream = (getStream: () => Promise<ReadableStream<Object>>, deps: any[] = []) => {
    const [state, setState] = useState<StreamState>({ data: [], error: null, loading: false });
    useEffect(() => {
        let isMounted = true;

        const fetchData = async () => {
            setState({ data: [], error: null, loading: true });
            try {
                const stream = await getStream();
                const reader = stream.getReader();
                let result;
                let dataChunks: any[] = [];

                while (!(result = await reader.read()).done) {
                    if (isMounted) {
                        dataChunks.push(result.value);
                    }
                }

                if (isMounted) {
                    setState({ data: dataChunks, error: null, loading: false });
                }
            } catch (err) {
                if (isMounted) {
                    setState({ data: [], error: err as Error, loading: false });
                }
            }
        };

        fetchData();

        return () => {
            isMounted = false;
        };
    }, deps);

    return state;
};

export default useReadableStream;