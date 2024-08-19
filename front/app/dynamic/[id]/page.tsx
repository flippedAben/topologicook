export default function Dynamic({ params }: { params: { id: string } }) {
  const { id } = params;
  return <h1>Dynamic page: {id}</h1>;
}
