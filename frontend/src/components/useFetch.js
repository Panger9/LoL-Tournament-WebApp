import { useEffect, useState } from "react";

const useFetch = (url, options = {}, dependencies = []) => {
  const [data, setData] = useState(null);
  const [isPending, setIsPending] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(url, {...options});
        if (!res.ok) {
          console.log()
          throw new Error(res.statusText + ' ' +  res.status);
        }
        const data = await res.json();
        setData(data);
        setIsPending(false);
        setError(null);
      } catch (err) {
        setError(err.message);
        setIsPending(false);
      }
    };

    fetchData();
  }, [url, ...dependencies]);

  return { data, isPending, error };
};

const useGet = (url, dependencies = []) => {
  return useFetch(url, { method: 'GET' }, dependencies);
};

const usePost = (url, body, dependencies = []) => {
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  };
  return useFetch(url, options, dependencies);
};

const usePut = (url, body, dependencies = []) => {
  const options = {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  };
  return useFetch(url, options, dependencies);
};

const useDelete = (url, dependencies = []) => {
  return useFetch(url, { method: 'DELETE' }, dependencies);
};

export { useGet, usePost, usePut, useDelete };

